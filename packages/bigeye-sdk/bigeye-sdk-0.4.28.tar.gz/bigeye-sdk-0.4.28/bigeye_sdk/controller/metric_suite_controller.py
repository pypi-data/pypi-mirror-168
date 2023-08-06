import os.path
import sys
from pathlib import Path
from typing import List, Dict, Tuple

from bigeye_sdk.bigconfig_validation.big_config_reports import raise_files_contain_error_exception, MetricSuiteReport, \
    process_reports, ProcessStage
from bigeye_sdk.bigconfig_validation.validation_context import process_validation_errors, \
    get_validation_error_cnt, get_file_error_match_cnt, get_all_validation_erros_flat
from bigeye_sdk.bigconfig_validation.yaml_validation_error_messages import SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG, \
    METRIC_APPLICATION_ERROR
from bigeye_sdk.client.datawatch_client import DatawatchClient
from bigeye_sdk.exceptions.exceptions import FileLoadException, BigConfigValidationException, NoSourcesFoundException
from bigeye_sdk.functions.bigconfig_functions import explode_fq_column_selectors
from bigeye_sdk.functions.metric_functions import _is_table_level_metric
from bigeye_sdk.functions.search_and_match_functions import wildcard_search
from bigeye_sdk.generated.com.torodata.models.generated import Source, CohortDefinition, \
    MetricSuite, CohortAndMetricDefinition, CatalogEntityType, MetricDefinition
from bigeye_sdk.model.big_config import BigConfig, RowCreationTimes, TagDeployment, TableDeployment
from bigeye_sdk.model.protobuf_enum_facade import SimplePredefinedMetricName
from bigeye_sdk.model.protobuf_message_facade import SimpleSLA, SimpleMetricDefinition
from bigeye_sdk.serializable import File, BIGCONFIG_FILE


def get_fq_name_from_cohort(cohort: CohortDefinition, source_name: str = None):
    """
    Args:
        cohort: cohort for which to get fully_qualified_name
        source_name: (optional) if available will prepend source name.

    Returns: fully qualified name
    """
    if cohort.column_name_pattern:
        r = f'{cohort.schema_name_pattern}.{cohort.table_name_pattern}.{cohort.column_name_pattern}'
    else:
        r = f'{cohort.schema_name_pattern}.{cohort.table_name_pattern}'

    if not source_name:
        return r
    else:
        return f'{source_name}.{r}'


def _find_bigconfig_files(source_path: str = None) -> List[BIGCONFIG_FILE]:
    """
    Finds bigconfig files either in specified source path or in working directory
    Args:
        source_path: specify a source path or working directory will be used.

    Returns: None

    """
    files: List[Path]
    if source_path and os.path.isfile(source_path):
        files = [Path(source_path)]
    elif source_path and os.path.isdir(source_path):
        files = list(Path(source_path).glob('*.y*ml'))
    else:
        """Assumes driver run in directory containing Bigconfig YAML."""
        files = list(Path.cwd().glob('*.y*ml'))

    bigeye_files: List[BIGCONFIG_FILE] = []
    file: BIGCONFIG_FILE
    for file in files:
        try:
            """Loading Bigconfig YAML.  If file is not of Bigconfig type then the error will be caught and passed."""
            bigeye_files.append(File.load(str(file)))
        except FileLoadException:
            pass

    if len(bigeye_files) == 0:
        raise BigConfigValidationException(f'No conforming files found.')
    elif len(bigeye_files) > 1 or bigeye_files[0].type != 'BIGCONFIG_FILE':
        # TODO change once we allow additional files.
        raise BigConfigValidationException(f'Multiple files not currently supported.')

    else:
        return bigeye_files


class MetricSuiteController:

    def __init__(self, client: DatawatchClient):
        self.client = client

        self.sources_by_name_ix: Dict[str, Source] = self.client.get_sources_by_name()
        self.sources_by_id_ix: Dict[int, Source] = {v.id: v for k, v in self.sources_by_name_ix.items()}

        self.table_level_metrics: List[SimplePredefinedMetricName] = [
            SimplePredefinedMetricName.from_datawatch_object(pmn)
            for pmn in self.client.get_table_level_metrics().metric_names
        ]

    def _upsert_slas(self,
                     bigconfig: BigConfig,
                     overwrite: bool,
                     apply=False) -> List[SimpleSLA]:
        """
        Currently operates as an overwrite of existing metrics.  This prevents altering in the front end.  Every time the
        config is run it will overwrite what is already there.
        Args:
            bigconfig: Bigconfig.

        Returns: a list of upserted SLAs

        """
        existing_slas = {sla.name: sla for sla in self.client.get_collections().collections}
        deployment_slas = []

        for sla in bigconfig.get_slas():
            if sla.name in existing_slas.keys():
                existing = SimpleSLA.from_datawatch_object(existing_slas[sla.name])
                merged = sla.merge_for_upsert(existing=existing, overwrite=overwrite)
                deployment_slas.append(merged)
                if apply:
                    self.client.update_collection(collection=merged.to_datawatch_object())
            else:
                c = sla.to_datawatch_object()
                c = self.client.create_collection(
                    collection_name=c.name,
                    description=c.description,
                    metric_ids=c.metric_ids,
                    notification_channels=c.notification_channels,
                    muted_until_timestamp=c.muted_until_timestamp
                ).collection
                deployment_slas.append(SimpleSLA.from_datawatch_object(c))

        return deployment_slas

    def row_creation_times_to_cohort(self, row_creation_times: RowCreationTimes) -> Dict[int, List[CohortDefinition]]:
        r: Dict[int, List[CohortDefinition]] = {}

        for cs in row_creation_times.column_selectors:
            split: List[str] = explode_fq_column_selectors(cs.name)
            source_pattern = split[0]
            schema_pattern = split[1]
            table_pattern = split[2]
            column_pattern = split[3]

            matching_source_ids = [source.id
                                   for source_name, source in self.sources_by_name_ix.items()
                                   if source_name in wildcard_search(search_string=source_pattern,
                                                                     content=[source_name])
                                   ]

            if not matching_source_ids:
                "registering validation errors when the source was not matched."
                errlns = cs.get_error_lines()
                row_creation_times.register_validation_error(
                    error_lines=errlns,
                    error_message=SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG.format(fq_name=cs))

            for id in matching_source_ids:
                cd = CohortDefinition(schema_name_pattern=schema_pattern, table_name_pattern=table_pattern,
                                      column_name_pattern=column_pattern,
                                      entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_FIELD)
                if id in r.keys():
                    r[id].append(cd)
                else:
                    r[id] = [cd]

        return r

    def table_deployment_to_row_creation_times_cohort(self, td: TableDeployment) -> Dict[int, CohortDefinition]:
        r: Dict[int, CohortDefinition] = {}

        split: List[str] = td.explode_fq_table_name()
        source_pattern = split[0]
        schema_pattern = split[1]
        table_pattern = split[2]
        column_pattern = td.row_creation_time
        if column_pattern is None:
            return r

        matching_source_ids = [source.id
                               for source_name, source in self.sources_by_name_ix.items()
                               if source_name in wildcard_search(search_string=source_pattern,
                                                                 content=[source_name])
                               ]

        if not matching_source_ids:
            "registering validation errors when the source was not matched."
            errlns = [f"fq_table_name: {td.fq_table_name}"]
            td.register_validation_error(
                error_lines=errlns,
                error_message=SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG.format(fq_name=td))

        for id in matching_source_ids:
            cd = CohortDefinition(schema_name_pattern=schema_pattern, table_name_pattern=table_pattern,
                                  column_name_pattern=column_pattern,
                                  entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_FIELD)
            r[id] = cd

        return r

    def tag_deployment_to_cohort_and_metric_def(self,
                                                tag_deployment: TagDeployment,
                                                deployment_sla: SimpleSLA = None
                                                ) -> Dict[int, List[CohortAndMetricDefinition]]:
        """
        Builds a Cohort and MetricDefinition from a TagDeployment object.   For table level metrics
        Args:
            tag_deployment: tag deployment to convert to cohort and metric definitoin.
            deployment_sla: The sla associated with the deployment.

        Returns: Dict[source_id: int, List[CohortAndMetricDefinition]] matched based on source_id to consolidate to
        a single metric suite object.
        """

        cmds: Dict[int, List[CohortAndMetricDefinition]] = {}
        column_metrics: List[Tuple[SimpleMetricDefinition, MetricDefinition]] = []
        table_metrics: List[Tuple[SimpleMetricDefinition, MetricDefinition]] = []

        for m in tag_deployment.metrics:
            """segregate table level metrics from column level and add slas"""
            if deployment_sla and deployment_sla.id not in m.sla_ids:
                m.sla_ids.append(deployment_sla.id)
            mdwo = m.to_datawatch_object()
            if _is_table_level_metric(metric_type=m.metric_type, table_level_metrics=self.table_level_metrics):
                mdwo.is_table_metric = True
                table_metrics.append((m, mdwo))
            else:
                column_metrics.append((m, mdwo))

        for cs in tag_deployment.column_selectors:
            cse = explode_fq_column_selectors(cs.name)
            source_pattern = cse[0]
            schema_pattern = cse[1]
            table_pattern = cse[2]
            column_pattern = cse[3]

            matching_source_ids = [source.id
                                   for source_name, source in self.sources_by_name_ix.items()
                                   if source_name in wildcard_search(search_string=source_pattern,
                                                                     content=[source_name])
                                   ]

            if not matching_source_ids:
                "registering validation errors when the source was not matched."
                tag_deployment.register_validation_error(
                    error_lines=cs.get_error_lines(),
                    error_message=SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG.format(fq_name=cs))

            if column_metrics:
                """Only append cohorts if metrics actually exist."""
                columns_cohort = CohortDefinition(schema_name_pattern=schema_pattern, table_name_pattern=table_pattern,
                                                  column_name_pattern=column_pattern,
                                                  entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_FIELD)
                for sid in matching_source_ids:
                    """Tag deployments support source patterns.  Each source id becomes a key in the returned dictionary 
                    with the exact same cohorts and metrics."""
                    cmd = CohortAndMetricDefinition(cohorts=[columns_cohort], metrics=[i[1] for i in column_metrics])
                    if sid in cmds:
                        cmds[sid].append(cmd)
                    else:
                        cmds[sid] = [cmd]

            if table_metrics:
                if column_pattern != '*':
                    for smd, md in table_metrics:
                        errmsg = f"Table level metrics can only be applied to column selectors if the column is a " \
                                 f"wild card.  Column Selector: {cs.name}.  Metric: {smd.metric_type}.  " \
                                 f"Table level metrics include: {', '.join([i.name for i in self.table_level_metrics])}"
                        tag_deployment.register_validation_error(
                            error_lines=smd.get_error_lines(),
                            error_context_lines=tag_deployment.get_error_lines(),
                            error_message=METRIC_APPLICATION_ERROR.format(errmsg=errmsg))

                table_cohort = CohortDefinition(schema_name_pattern=schema_pattern, table_name_pattern=table_pattern,
                                                column_name_pattern=column_pattern,
                                                entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_DATASET)

                for sid in matching_source_ids:
                    """Tag deployments support source patterns.  Each source id becomes a key in the returned dictionary 
                    with the exact same cohorts and metrics."""
                    cmd = CohortAndMetricDefinition(cohorts=[table_cohort], metrics=[i[1] for i in table_metrics])
                    if sid in cmds:
                        cmds[sid].append(cmd)
                    else:
                        cmds[sid] = [cmd]

        return cmds

    def table_deployment_to_cohort_and_metric_def(self,
                                                  table_deployment: TableDeployment,
                                                  deployment_sla: SimpleSLA = None) -> Dict[
        int, List[CohortAndMetricDefinition]]:
        """
        Builds a Cohort and MetricDefinition from a TableDeployment object
        Args:
            table_deployment: table deployment from which to generate cohort and metric definition
            deployment_sla: SLA to which metrics will be added.

        Returns: Dict[warehouse_id: int, CohortAndMetricDefinition]
        """

        result: Dict[int, List[CohortAndMetricDefinition]] = {}

        fq_names_list = table_deployment.explode_fq_table_name()
        source_name = fq_names_list[0]
        schema_name = fq_names_list[1]
        table_name = fq_names_list[2]

        if source_name in self.sources_by_name_ix:
            sid = self.sources_by_name_ix[source_name].id
        else:
            "registering validation errors when the source was not matched."
            sid = 0
            error_message = SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG.format(fq_name=table_deployment.fq_table_name)
            table_deployment.register_validation_error(error_lines=[f"fq_table_name: {table_deployment.fq_table_name}"],
                                                       error_message=error_message)

        cmds: List[CohortAndMetricDefinition] = []

        table_metrics = []
        table_cohort = CohortDefinition(schema_name_pattern=schema_name, table_name_pattern=table_name,
                                        entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_DATASET)

        for m in table_deployment.table_metrics:
            "process table metrics and raise validation errors if column level metrics are defined."
            if not _is_table_level_metric(metric_type=m.metric_type, table_level_metrics=self.table_level_metrics):
                errmsg = f"Column level metrics cannot be applied at the table level.  " \
                         f"Table: {table_deployment.fq_table_name}.  " \
                         f"Metric: {m.metric_type} is a column level metric.  " \
                         f"Table level metrics include: {', '.join([i.name for i in self.table_level_metrics])}"

                table_deployment.register_validation_error(
                    error_lines=m.get_error_lines(),
                    error_context_lines=table_deployment.get_table_metrics_error_lines(),
                    error_message=METRIC_APPLICATION_ERROR.format(errmsg=errmsg)
                )
            else:
                if deployment_sla and deployment_sla.id not in m.sla_ids:
                    m.sla_ids.append(deployment_sla.id)
                mdwo = m.to_datawatch_object()
                mdwo.is_table_metric = True
                table_metrics.append(mdwo)

        if table_metrics:
            "Only add the cohort if metrics actually exist for it."
            cmds.append(
                CohortAndMetricDefinition(cohorts=[table_cohort], metrics=table_metrics)
            )

        for c in table_deployment.columns:
            "Process Column Metrics"
            cohort = CohortDefinition(schema_name_pattern=schema_name, table_name_pattern=table_name,
                                      column_name_pattern=c.column_name,
                                      entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_FIELD)
            col_metrics = []

            for m in c.metrics:
                if _is_table_level_metric(metric_type=m.metric_type, table_level_metrics=self.table_level_metrics):
                    errmsg = f"Table level metrics cannot be applied at the column level.  " \
                             f"Table: {table_deployment.fq_table_name}.  Column: {c.column_name}.  " \
                             f"Metric: {m.metric_type} is a table level metric.  " \
                             f"Table level metrics include: {', '.join([i.name for i in self.table_level_metrics])}"

                    table_deployment.register_validation_error(
                        error_lines=m.get_error_lines(),
                        error_context_lines=table_deployment.get_error_lines(),
                        error_message=METRIC_APPLICATION_ERROR.format(errmsg=errmsg)
                    )
                else:
                    if deployment_sla and deployment_sla.id not in m.sla_ids:
                        m.sla_ids.append(deployment_sla.id)
                    mdwo = m.to_datawatch_object()
                    col_metrics.append(mdwo)

            if col_metrics:
                "Only add the cohort if metrics actually exist for it."
                cmds.append(
                    CohortAndMetricDefinition(cohorts=[cohort], metrics=col_metrics))

        result[sid] = cmds

        return result

    def bigconfig_to_metric_suites(self,
                                   bigconfig: BigConfig,
                                   deployment_slas: Dict[str, SimpleSLA]) -> List[MetricSuite]:
        """
        Creates a MetricSuite for each source identified in a Bigconfig Table or Tag Deployment.
        Args:
            bigconfig: Bigconfig from which MetricSuites will be created.
            deployment_slas: Upserted SLAs (must contain ID)

        Returns: List[MetricSuite]
        """

        # Applying metric suites after instantiation so that validation errors early on can be located in files.
        bigconfig.apply_tags_and_saved_metrics()

        cmds: Dict[int, List[CohortAndMetricDefinition]] = {}

        rct_cohorts: Dict[int, List[CohortDefinition]] = self.row_creation_times_to_cohort(bigconfig.row_creation_times)

        for tag_d_suite in bigconfig.tag_deployments:
            for tag_d in tag_d_suite.deployments:
                """Process all tag deployments into CohortAndMetricDefinitions.  One tag deployment per CMD"""
                if tag_d_suite.sla:
                    deployment_sla = deployment_slas.get(tag_d_suite.sla.name, None)
                else:
                    deployment_sla = None
                r: Dict[int, List[CohortAndMetricDefinition]] = self.tag_deployment_to_cohort_and_metric_def(
                    tag_deployment=tag_d,
                    deployment_sla=deployment_sla
                )
                for sid, definitions in r.items():
                    """consolidate based on source"""
                    if sid in cmds:
                        cmds[sid].extend(definitions)
                    else:
                        cmds[sid] = definitions

        for table_d_suite in bigconfig.table_deployments:
            for table_d in table_d_suite.deployments:
                "Process all table deployments into CohortAndMetricDefinitions. One table deployment per CMD"
                if table_d_suite.sla:
                    deployment_sla = deployment_slas.get(table_d_suite.sla.name, None)
                else:
                    deployment_sla = None
                r = self.table_deployment_to_cohort_and_metric_def(
                    table_deployment=table_d,
                    deployment_sla=deployment_sla
                )
                for sid, definitions in r.items():
                    """consolidate based on sources"""
                    if sid in cmds:
                        cmds[sid].extend(definitions)
                    else:
                        cmds[sid] = definitions
                rct = self.table_deployment_to_row_creation_times_cohort(table_d)
                for sid, cohorts in rct.items():
                    if sid in rct_cohorts.keys():
                        rct_cohorts[sid].append(cohorts)
                    else:
                        rct_cohorts[sid] = [cohorts]

        deployment_metric_suites: Dict[int, MetricSuite] = {
            source_id: MetricSuite(source_id=source_id, definitions=definitions)
            for source_id, definitions in cmds.items()
        }

        metric_suites: List[MetricSuite] = []

        for source_id, metric_suite in deployment_metric_suites.items():
            if source_id in rct_cohorts.keys():
                metric_suite.row_creation_cohorts = rct_cohorts.pop(source_id)

            metric_suites.append(metric_suite)

        for source_id, rcts in rct_cohorts.items():
            metric_suites.append(
                MetricSuite(source_id=source_id, row_creation_cohorts=rcts)
            )

        return metric_suites

    def execute_purge(self, purge_source_names: List[str] = None,
                      purge_all_sources: bool = False,
                      output_path: str = Path.cwd(), apply: bool = False):
        """
        Executes a purge of metrics deployed by MetricSuite on named sources or for all sources.
        Args:
            purge_source_names: list of source names to purge
            purge_all_sources: if true will purge all sources.
            output_path: path to dump the reports.  If no path is given the current working directory will be used.
            apply: If true then Big Config will be applied to the workspace.  If false then a plan will be generated.
        """
        try:
            self.client.purge_metric_suites(source_names=purge_source_names,
                                            purge_all_sources=purge_all_sources,
                                            apply=apply
                                            )
            process_reports(output_path=output_path)
        except NoSourcesFoundException as e:
            sys.exit(e.message)

    def execute_bigconfig(self,
                          input_path: str = Path.cwd(),
                          output_path: str = Path.cwd(), apply: bool = False):
        """
        Executes an Apply or Plan for a Big Config.
        Args:
            input_path: path of source files.  If no path is given the current working directory will be used.
            output_path: path to dump the reports.  If no path is given the current working directory will be used.
            apply: If true then Big Config will be applied to the workspace.  If false then a plan will be generated.

        Returns: None

        """
        files: List[BIGCONFIG_FILE] = _find_bigconfig_files(input_path)

        bigconfig: BigConfig = files[0]

        if get_validation_error_cnt():
            """Processing validation errors if any exist and throw exception."""
            fixme_file_list = process_validation_errors(output_path)
            unmatched_validations_errors = get_all_validation_erros_flat(only_unmatched=True)
            raise_files_contain_error_exception(validation_error_cnt=get_validation_error_cnt(),
                                                unmatched_validations_errors=unmatched_validations_errors,
                                                fixme_file_list=fixme_file_list)

        deployment_slas = {sla.name: sla for sla in self._upsert_slas(bigconfig, False)}

        metric_suites = self.bigconfig_to_metric_suites(bigconfig=bigconfig, deployment_slas=deployment_slas)

        if get_validation_error_cnt():
            """Processing validation errors if any exist and throw exception."""
            fixme_file_list = process_validation_errors(output_path)
            unmatched_validations_errors = get_all_validation_erros_flat(only_unmatched=True)
            raise_files_contain_error_exception(validation_error_cnt=get_validation_error_cnt(),
                                                unmatched_validations_errors=unmatched_validations_errors,
                                                fixme_file_list=fixme_file_list)

        if apply:
            self._upsert_slas(bigconfig, True)  # Will always overwrite for Bigconfig.

        for metric_suite in metric_suites:
            j = metric_suite.to_json()
            response = self.client.post_metric_suite(metric_suite=metric_suite, apply=apply)
            process_stage = ProcessStage.APPLY if apply else ProcessStage.PLAN
            MetricSuiteReport.from_datawatch_object(response,
                                                    source_name=self.sources_by_id_ix[metric_suite.source_id].name,
                                                    process_stage=process_stage)

        process_reports(output_path=output_path)
