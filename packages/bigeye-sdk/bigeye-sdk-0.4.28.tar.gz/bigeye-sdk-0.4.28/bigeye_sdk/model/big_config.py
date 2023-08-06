from __future__ import annotations

from typing import List, Optional, Dict, Tuple, Any

import yaml
from pydantic import Field, PrivateAttr, validator, root_validator

from bigeye_sdk.bigconfig_validation.validation_functions import safe_split_dict_entry_lines, must_be_list_validator
from bigeye_sdk.bigconfig_validation.yaml_model_base import YamlModelWithValidatorContext
from bigeye_sdk.bigconfig_validation.yaml_validation_error_messages import DUPLICATE_SAVED_METRIC_ID_EXISTS_ERRMSG, \
    DUPLICATE_TAG_EXISTS_ERRMSG, TAG_ID_NOT_EXISTS_IN_TAG_DEFINITION_ERRMSG, \
    SAVED_METRIC_ID_NOT_EXISTS_IN_SAVED_METRICS_DEFINITION_ERRMSG, FQ_COL_NOT_RESOLVES_TO_COLUMN_ERRMSG, \
    WILD_CARDS_NOT_SUPPORT_IN_FQ_TABLE_NAMES_ERRMSG, FQ_TABLE_NAME_MUST_RESOLVE_TO_TABLE_ERRMSG
from bigeye_sdk.functions.bigconfig_functions import explode_fq_name, explode_fq_column_selectors, \
    explode_fq_table_name
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.protobuf_message_facade import SimpleMetricDefinition, SimpleSLA
from bigeye_sdk.serializable import BigConfigFile

log = get_logger(__file__)


class ColumnSelector(YamlModelWithValidatorContext):
    name: str

    # types: List[SimpleFieldType] TODO V1

    @validator('name')
    def must_have_split_length_4_or_5(cls, v):
        if v == '' or len(v) == 0 or len(explode_fq_name(v)) not in [4, 5]:
            error_message = FQ_COL_NOT_RESOLVES_TO_COLUMN_ERRMSG.format(fq_column_name=v)
            cls.register_validation_error(error_lines=[v], error_message=error_message)

        return v

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        if not isinstance(other, ColumnSelector):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.name == other.name


class TagDefinition(YamlModelWithValidatorContext):
    tag_id: str
    column_selectors: List[ColumnSelector]

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TagDefinition, attribute_name='column_selectors', values=values)

        return values
    def __hash__(self):
        return hash((repr(self.tag_id), self.column_selectors))


# @dataclass
# class SavedMetricCollection:
#     collection_name: str
#     saved_metric_ids: List[str]


class SavedMetricDefinitions(YamlModelWithValidatorContext):
    # metric_collections: SavedMetricCollection
    metrics: List[SimpleMetricDefinition]

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=SavedMetricDefinitions, attribute_name='metrics', values=values)

        return values

class RowCreationTimes(YamlModelWithValidatorContext):
    tag_ids: Optional[List[str]] = Field(default_factory=lambda: [])
    column_selectors: Optional[List[ColumnSelector]] = Field(default_factory=lambda: [])

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=RowCreationTimes, attribute_name='tag_ids', values=values)
        must_be_list_validator(clazz=RowCreationTimes, attribute_name='column_selectors', values=values)

        return values


class TagDeployment(YamlModelWithValidatorContext):
    metrics: List[SimpleMetricDefinition]
    tag_id: Optional[str] = None
    column_selectors: Optional[List[ColumnSelector]] = Field(default_factory=lambda: [])

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TagDeployment, attribute_name='metrics', values=values)
        must_be_list_validator(clazz=TagDeployment, attribute_name='column_selectors', values=values)

        return values

    def explode_fq_column_selectors(self) -> List[List[str]]:
        """
        Explodes a fully qualifeid column selectors into a list of names.  Supports wild cards as *. Supports single and
        double quoted  names containing periods.  Supports fully qulified names with either source.database.schema or
        source.schema convention.

            Example: wh."my.*".some_*_table.* resolves to ['wh', 'my.*', 'some_*_table', '*']

        Returns: list of names from each fully qualified column selector in the Tag Deployment
        """
        return [explode_fq_column_selectors(i.name) for i in self.column_selectors]


class TagDeploymentSuite(YamlModelWithValidatorContext):
    deployments: List[TagDeployment]
    sla: Optional[SimpleSLA] = None

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TagDeploymentSuite, attribute_name='deployments', values=values)

        return values

    @validator('deployments', each_item=True)
    def validate_metric_business_rules(cls, v: TagDeployment):
        for m in v.metrics:
            m.deployment_validations(config_error_lines=v.get_error_lines())

        return v


class ColumnMetricDeployment(YamlModelWithValidatorContext):
    column_name: str
    metrics: List[SimpleMetricDefinition]

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TableDeployment, attribute_name='metrics', values=values)

        return values

class TableDeployment(YamlModelWithValidatorContext):
    fq_table_name: str
    columns: Optional[List[ColumnMetricDeployment]] = Field(default_factory=lambda: [])
    table_metrics: Optional[List[SimpleMetricDefinition]] = Field(default_factory=lambda: [])
    row_creation_time: Optional[str] = None

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TableDeployment, attribute_name='columns', values=values)
        must_be_list_validator(clazz=TableDeployment, attribute_name='table_metrics', values=values)

        return values

    @validator('fq_table_name')
    def fq_table_name_must_not_have_wildcards(cls, v):
        if '*' in v:
            error_message = WILD_CARDS_NOT_SUPPORT_IN_FQ_TABLE_NAMES_ERRMSG.format(fq_table_name=v)
            cls.register_validation_error(error_lines=[v], error_message=error_message)

        return v

    @validator('fq_table_name')
    def must_have_split_length_3_or_4(cls, v):
        if v == '' or len(v) == 0 or len(explode_fq_name(v)) not in [3, 4]:
            error_message = FQ_TABLE_NAME_MUST_RESOLVE_TO_TABLE_ERRMSG.format(fq_table_name=v)
            cls.register_validation_error(error_lines=[v], error_message=error_message)
        return v

    @validator('columns', each_item=True)
    def validate_metric_business_rules_for_columns(cls, v: ColumnMetricDeployment):
        """Document in deployment_validations()"""
        error_config_lines = v.get_error_lines()

        for m in v.metrics:
            m.deployment_validations(error_config_lines)

        return v

    def get_table_metrics_error_lines(self):
        return safe_split_dict_entry_lines(
            'table_metrics',
            [smd.get_error_lines() for smd in self.table_metrics])

    def explode_fq_table_name(self):
        """
        Explodes a fully qualifeid table name into a list of names.  Supports single and double quoted  names
        containing periods.  Supports fully qulified names with either source.database.schema or source.schema
        conventions.  DOES NOT support wild cards.

            Example: wh."my.schema".some_table resolves to ['wh', 'my.schema', 'some_table']

        Returns: list of names from the fully qualified table name
        """

        return explode_fq_table_name(self.fq_table_name)


class TableDeploymentSuite(YamlModelWithValidatorContext):
    deployments: List[TableDeployment]
    sla: Optional[SimpleSLA] = None

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TableDeploymentSuite, attribute_name='deployments', values=values)

        return values

    @validator('deployments', each_item=True)
    def validate_metric_business_rules_for_table_metrics(cls, v: TableDeployment):
        for m in v.table_metrics:
            m.deployment_validations(config_error_lines=v.get_error_lines())
        return v


class BigConfig(BigConfigFile, type='BIGCONFIG_FILE'):
    """
    Bigconfig is a canonical model used to collate and compile all definition and deployment files maintained by users
    into a single object that can be used to generate a metric suite.  Tag Definitions and Saved Metric Definitions
    are applied -- and validated -- during the __post_init__ phase of instantiating a Bigconfig.
    """
    tag_definitions: Optional[List[TagDefinition]] = Field(
        default_factory=lambda: [])  # only one because we must consolidate if creating Bigconfig from multiple files.
    row_creation_times: Optional[RowCreationTimes] = RowCreationTimes()
    saved_metric_definitions: Optional[
        SavedMetricDefinitions] = None  # only one because we must consolidate if creating Bigconfig from multiple files.
    tag_deployments: Optional[List[TagDeploymentSuite]] = Field(default_factory=lambda: [])
    table_deployments: Optional[List[TableDeploymentSuite]] = Field(default_factory=lambda: [])

    _tag_ix_: Dict[str, List[ColumnSelector]] = PrivateAttr({})  # Dict[tag_id, List[ColumnSelector]]
    _saved_metric_ix_: Dict[str, SimpleMetricDefinition] = PrivateAttr(
        {})  # Dict[saved_metric_id, SimpleMetricDefinition]

    # _saved_metric_collection_ix_: Dict[str, List, str] = {}  # Dict[saved_metric_collection_id, List[saved_metric_id]] (V1)

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=BigConfig, attribute_name='tag_definitions', values=values)
        must_be_list_validator(clazz=BigConfig, attribute_name='tag_deployments', values=values)
        must_be_list_validator(clazz=BigConfig, attribute_name='table_deployments', values=values)

        return values

    @validator('saved_metric_definitions')
    def each_saved_metric_must_have_id(cls, v: SavedMetricDefinitions):
        """Located here to capture the full configurations lines for error.  Validators can be weird.  Could use
        root_validator in the future."""
        config_error_lines: List[str] = v.get_error_lines()
        for m in v.metrics:
            m.saved_metrics_must_have_id(config_error_lines=config_error_lines)
        return v

    def __init__(self, **data: Any):
        super().__init__(**data)

        log.info('Building Indices.')
        if self.tag_definitions:
            self._tag_ix_ = self._generate_tag_ix(self.tag_definitions)

        if self.saved_metric_definitions:
            self._saved_metric_ix_ = self._generate_saved_metric_def_ix(self.saved_metric_definitions)

    def apply_tags_and_saved_metrics(self):

        log.info('Applying tags and saved metrics.')

        if self._tag_ix_:
            apply_result = self._apply_tags(tag_ix=self._tag_ix_, tag_deps=self.tag_deployments,
                                            row_creation_times=self.row_creation_times)
            self.tag_deployments = apply_result[0]
            self.row_creation_times = apply_result[1]

        if self._saved_metric_ix_:
            apply_result = self._apply_saved_metrics(saved_metric_ix=self._saved_metric_ix_,
                                                     tag_deps=self.tag_deployments,
                                                     table_deps=self.table_deployments)
            self.tag_deployments = apply_result[0]
            self.table_deployments = apply_result[1]

    @classmethod
    def _generate_tag_ix(cls, tag_definitions: List[TagDefinition]) -> Dict[str, List[ColumnSelector]]:
        """
        Generates an index of Column Selectors by Tag ID and validates no duplicates exist and that column selectors
        is not empty.
        Args:
            tag_definitions: List of Tag Definitions from which an Index will be generated.

        Returns: An index of Column Selectors by Tag ID.
        """
        tix: Dict[str, List[ColumnSelector]] = {}
        for td in tag_definitions:
            if td.tag_id in tix:
                error_message = DUPLICATE_TAG_EXISTS_ERRMSG.format(tag_id=td.tag_id)
                cls.register_validation_error(error_context_lines=td.get_error_lines(),
                                              error_lines=[td.tag_id],
                                              error_message=error_message)

            tix[td.tag_id] = td.column_selectors

        return tix

    @classmethod
    def _generate_saved_metric_def_ix(cls, smd: SavedMetricDefinitions) -> Dict[str, SimpleMetricDefinition]:
        """
        Generates an index of Saved Metric Definitions by Saved Metric ID and validates no duplicates exist and that
        the Metric Definitions defined have at least a `saved_metric_id` and a `metric_type`.
        Args:
            smd: a Saved Metric Definitions object from which the Saved Metric Definitions IX will be generated.

        Returns: An index of Simple Metric Definitions keyed by `saved_metric_id`.

        """
        smdix: Dict[str, SimpleMetricDefinition] = {}
        for m in smd.metrics:
            if m.saved_metric_id in smdix:
                error_message = DUPLICATE_SAVED_METRIC_ID_EXISTS_ERRMSG.format(
                    saved_metric_id=m.saved_metric_id
                )
                test = m.get_error_lines()
                err_lines = [yaml.safe_dump({'saved_metric_id': m.saved_metric_id}, indent=True, sort_keys=False)]
                # TODO Removed the context lines because when nested bugs exist in yaml and some of them are caught as
                # TODO pre/raw bugs then we might have already fixed the issue (manipulated the values) so we could
                # TODO capture post/object bugs.  This would break the search.
                # cls.register_validation_error(error_context_lines=smd.get_error_lines(),
                #                               error_lines=err_lines,
                #                               error_message=error_message)
                cls.register_validation_error(error_lines=err_lines,
                                              error_message=error_message)

            if m.saved_metric_id:
                smdix[m.saved_metric_id] = m

        return smdix

    @classmethod
    def _tag_id_exists_in_ix(cls, tag_id: str, tag_ix: Dict[str, List[ColumnSelector]]) -> bool:
        if tag_id not in tag_ix:
            error_message = TAG_ID_NOT_EXISTS_IN_TAG_DEFINITION_ERRMSG.format(tag_id=tag_id)
            cls.register_validation_error(error_lines=[tag_id],
                                          error_message=error_message)
            return False
        else:
            return True

    @classmethod
    def _apply_tags(cls, tag_ix: Dict[str, List[ColumnSelector]],
                    tag_deps: List[TagDeploymentSuite],
                    row_creation_times: RowCreationTimes) -> Tuple[List[TagDeploymentSuite], RowCreationTimes]:
        """
        Applies tags by tag id in all tag deployments and row creation times definitinos.  Validates that all tags
        called in deployments exist in the tags definitions.  Validates that column selectors exist after application.
        Args:
            tag_ix: index of column selectors keyed by tag_id
            tag_deps: list of Tag Deployment Suites to which tags will be applied.
            row_creation_times: row creation times to which tags will be applied

        Returns: list of Tag Deployment Suites to which tags have been applied.

        """

        for td in tag_deps:
            for d in td.deployments:
                if d.tag_id and cls._tag_id_exists_in_ix(d.tag_id, tag_ix):
                    tagged_col_selectors = tag_ix.get(d.tag_id, [])
                    d.column_selectors.extend(tagged_col_selectors)
                    d.column_selectors = sorted(list(set(d.column_selectors)))

        for tag_id in row_creation_times.tag_ids:
            if cls._tag_id_exists_in_ix(tag_id, tag_ix):
                row_creation_times.column_selectors.extend(tag_ix[tag_id])

        row_creation_times.column_selectors = sorted(list(set(row_creation_times.column_selectors)))

        return tag_deps, row_creation_times

    @classmethod
    def _validate_and_apply(cls, m: SimpleMetricDefinition,
                            saved_metric_ix: Dict[str, SimpleMetricDefinition]) -> SimpleMetricDefinition:

        def _apply_overrides(saved_smd: SimpleMetricDefinition,
                             override_smd: SimpleMetricDefinition) -> SimpleMetricDefinition:
            r = SimpleMetricDefinition(**saved_smd.dict())

            for attr in override_smd.__dict__.keys():
                override_attr_value = getattr(override_smd, attr)
                if attr not in ['saved_metric_id', 'metric_type', 'sla_ids'] \
                        and not SimpleMetricDefinition.is_default_value(attr, override_attr_value):
                    setattr(r, attr, override_attr_value)

            return r

        if not m.saved_metric_id:
            return m

        if m.saved_metric_id not in saved_metric_ix.keys():
            error_message = SAVED_METRIC_ID_NOT_EXISTS_IN_SAVED_METRICS_DEFINITION_ERRMSG.format(
                saved_metric_id=m.saved_metric_id)
            cls.register_validation_error(error_lines=m.get_error_lines(),
                                          error_message=error_message)
            return m
        else:
            saved = saved_metric_ix[m.saved_metric_id]
            return _apply_overrides(saved, m)

    @classmethod
    def _apply_saved_metrics(cls, saved_metric_ix: Dict[str, SimpleMetricDefinition],
                             tag_deps: List[TagDeploymentSuite],
                             table_deps: List[TableDeploymentSuite]
                             ) -> Tuple[List[TagDeploymentSuite], List[TableDeploymentSuite]]:

        for tag_dep in tag_deps:
            for d in tag_dep.deployments:
                metrics: List[SimpleMetricDefinition] = []
                for m in d.metrics:
                    metrics.append(cls._validate_and_apply(m, saved_metric_ix))
                d.metrics = metrics

        for table_dep in table_deps:
            for d in table_dep.deployments:
                table_metrics: List[SimpleMetricDefinition] = []
                for m in d.table_metrics:
                    table_metrics.append(cls._validate_and_apply(m, saved_metric_ix))
                d.table_metrics = table_metrics

                for c in d.columns:
                    column_metrics: List[SimpleMetricDefinition] = []
                    for m in c.metrics:
                        column_metrics.append(cls._validate_and_apply(m, saved_metric_ix))
                    c.metrics = column_metrics

        return tag_deps, table_deps

    def get_slas(self) -> List[SimpleSLA]:
        slas: List[SimpleSLA] = []

        for d in self.tag_deployments:
            if d.sla:
                slas.append(d.sla)

        for d in self.table_deployments:
            if d.sla:
                slas.append(d.sla)

        return slas
