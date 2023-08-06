from __future__ import annotations

import enum
import re
import sys
from abc import ABC
from collections.abc import Iterable
from typing import List, Optional, TypeVar, Union, Any

import betterproto
import yaml
from pydantic import validator, Field, root_validator
from pydantic_yaml import YamlIntEnum, YamlStrEnum

from bigeye_sdk.bigconfig_validation.validation_functions import safe_split_dict_entry_lines, must_be_list_validator
from bigeye_sdk.bigconfig_validation.yaml_model_base import YamlModelWithValidatorContext
from bigeye_sdk.bigconfig_validation.yaml_validation_error_messages import FORMATTING_ERRMSG, \
    OVERRIDE_METRIC_TYPE_SAVED_METRIC_ERRMSG, MUST_HAVE_METRIC_TYPE_ERRMSG, MUST_HAVE_METRIC_ID_ERRMSG, \
    METRIC_TYPE_NOT_EXISTS_ERRMSG, POSSIBLE_MATCH_ERRMSG, NO_POSSIBLE_MATCH_ERRMSG
from bigeye_sdk.exceptions import InvalidConfigurationException
from bigeye_sdk.functions.search_and_match_functions import fuzzy_match
from bigeye_sdk.functions.table_functions import get_table_column_id
from bigeye_sdk.generated.com.torodata.models.generated import Threshold, SimpleBoundType, ConstantThreshold, \
    SimpleBound, NamedSchedule, ComparisonColumnMapping, Table, IdAndDisplayName, ColumnNamePair, TimeInterval, \
    MetricParameter, MetricType, PredefinedMetric, TemplateMetric, AutoThreshold, ForecastModelType, RelativeThreshold, \
    StandardDeviationThreshold, FreshnessScheduleThreshold, NotificationChannel, MetricDefinition, MetricConfiguration, \
    Collection
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.base_datawatch_facade import DatawatchFacade
from bigeye_sdk.model.protobuf_enum_facade import SimplePredefinedMetricName, SimpleTimeIntervalType, \
    SimpleAutothresholdSensitivity, SimpleLookbackType, SimpleAggregationType
from bigeye_sdk.serializable import PydanticSubtypeSerializable

log = get_logger(__file__)


def get_type_from_dict(obj: betterproto.Message) -> str:
    """A patch for beterproto.which_one_of not working on objects serialized from_dict.   I have reported the bug to
    the maintainers of better proto.  TODO remove when bug is fixed."""
    return list(obj.to_dict(casing=betterproto.Casing.SNAKE).keys())[0]


class SimpleMetricType(PydanticSubtypeSerializable, DatawatchFacade, ABC):
    type: str

    @classmethod
    def get_freshness_metric_types(cls) -> List[SimplePredefinedMetric]:
        freshness_metric_names = [SimplePredefinedMetricName.HOURS_SINCE_LAST_LOAD,
                                  SimplePredefinedMetricName.HOURS_SINCE_MAX_DATE,
                                  SimplePredefinedMetricName.HOURS_SINCE_MAX_TIMESTAMP]
        return [SimplePredefinedMetric(type="PREDEFINED", metric=i) for i in freshness_metric_names]

    @classmethod
    def from_datawatch_object(cls, obj: MetricType) -> SimpleMetricType:
        t = betterproto.which_one_of(obj, "metric_type")[0]
        if not t:
            t = get_type_from_dict(obj)
        if t == 'template_metric':
            tm = obj.template_metric
            return SimpleTemplateMetric(type='TEMPLATE',
                                        template_id=tm.template_id,
                                        aggregation_type=SimpleAggregationType.from_datawatch_object(
                                            tm.aggregation_type),
                                        template_name=tm.template_name)
        elif t == 'predefined_metric':
            return SimplePredefinedMetric(
                type='PREDEFINED',
                metric=SimplePredefinedMetricName.from_datawatch_object(obj.predefined_metric.metric_name)
            )
        else:
            error_message = f"Metric type not supported: {t}"
            raise InvalidConfigurationException(error_message)


class SimplePredefinedMetric(SimpleMetricType, type='PREDEFINED'):
    metric: SimplePredefinedMetricName

    @validator('metric', pre=True)
    def must_be_valid_metric(cls, v):
        try:
            return SimplePredefinedMetricName(v)
        except ValueError:
            is_freshness = fuzzy_match(v,
                                       ['FRESHNESS'],
                                       85)
            possible_matches = fuzzy_match(v,
                                           [e.value for e in SimplePredefinedMetricName],
                                           50)
            if is_freshness:
                possible_match_message = POSSIBLE_MATCH_ERRMSG.format(
                    possible_matches=", ".join([
                        SimplePredefinedMetricName.HOURS_SINCE_MAX_DATE,
                        SimplePredefinedMetricName.HOURS_SINCE_MAX_TIMESTAMP
                    ]))
            elif possible_matches:
                pms = [i[1] for i in possible_matches][:3]
                possible_match_message = POSSIBLE_MATCH_ERRMSG.format(possible_matches=", ".join(pms))
            else:
                possible_match_message = NO_POSSIBLE_MATCH_ERRMSG

            error_message = METRIC_TYPE_NOT_EXISTS_ERRMSG.format(metric=v, match_message=possible_match_message)
            cls.register_validation_error(error_lines=[v],
                                          error_message=error_message)
            return SimplePredefinedMetricName.UNDEFINED

    def to_datawatch_object(self, **kwargs) -> MetricType:
        return MetricType(predefined_metric=PredefinedMetric(metric_name=self.metric.to_datawatch_object()))


class SimpleTemplateMetric(SimpleMetricType, type='TEMPLATE'):
    template_id: int
    aggregation_type: SimpleAggregationType
    template_name: Optional[str] = None

    def to_datawatch_object(self, **kwargs) -> MetricType:
        return MetricType(template_metric=TemplateMetric(template_id=self.template_id,
                                                         aggregation_type=self.aggregation_type.to_protpbuf(),
                                                         template_name=self.template_name))


class SimpleNamedSchedule(YamlModelWithValidatorContext, DatawatchFacade):
    name: str
    cron: str
    id: Optional[int] = None

    @classmethod
    def from_datawatch_object(cls, obj: NamedSchedule, **kwargs) -> SimpleNamedSchedule:
        return SimpleNamedSchedule(name=obj.name, cron=obj.cron, id=obj.id)

    def to_datawatch_object(self) -> NamedSchedule:
        return NamedSchedule(name=self.name, cron=self.cron, id=self.id)


class SimpleColumnMapping(YamlModelWithValidatorContext, DatawatchFacade):
    source_column_name: str
    target_column_name: str
    metrics: List[SimpleMetricType]

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=SimpleColumnMapping, attribute_name='metrics', values=values)

        return values

    @classmethod
    def from_datawatch_object(cls, obj: ComparisonColumnMapping) -> SimpleColumnMapping:
        smt_list: List[SimpleMetricType] = [SimpleMetricType.from_datawatch_object(om) for om in obj.metrics]
        return SimpleColumnMapping(source_column_name=obj.source_column.display_name,
                                   target_column_name=obj.target_column.display_name,
                                   metrics=smt_list)

    def to_datawatch_object(self, source_table: Table, target_table: Table) -> ComparisonColumnMapping:
        cm = ComparisonColumnMapping()
        cm.source_column = IdAndDisplayName(id=get_table_column_id(source_table, self.source_column_name),
                                            display_name=self.source_column_name)
        cm.target_column = IdAndDisplayName(id=get_table_column_id(target_table, self.target_column_name),
                                            display_name=self.target_column_name)
        cm.metrics = [m.to_datawatch_object() for m in self.metrics]
        return cm


class SimpleColumnPair(YamlModelWithValidatorContext, DatawatchFacade):
    source_column_name: str
    target_column_name: str

    @classmethod
    def from_datawatch_object(cls, obj: ColumnNamePair) -> SimpleColumnPair:
        return SimpleColumnPair(source_column_name=obj.source_column_name, target_column_name=obj.target_column_name)

    def to_datawatch_object(self) -> ColumnNamePair:
        return ColumnNamePair(
            source_column_name=self.source_column_name,
            target_column_name=self.target_column_name
        )


class SimpleTimeInterval(YamlModelWithValidatorContext, DatawatchFacade):
    interval_type: SimpleTimeIntervalType
    interval_value: int = 0

    @classmethod
    def from_datawatch_object(cls, obj: TimeInterval) -> Optional[SimpleTimeInterval]:
        if obj.interval_type == 0 and obj.interval_value == 0:
            return None
        return SimpleTimeInterval(interval_type=SimpleTimeIntervalType.from_datawatch_object(obj.interval_type),
                                  interval_value=obj.interval_value)

    def to_datawatch_object(self, **kwargs) -> TimeInterval:
        return TimeInterval(interval_type=self.interval_type.to_datawatch_object(), interval_value=self.interval_value)


ST = TypeVar('ST', bound='SimpleThreshold')


class SimpleThreshold(PydanticSubtypeSerializable, DatawatchFacade, ABC):
    type: str

    @classmethod
    def from_datawatch_object(cls, obj: List[Threshold]) -> ST:
        t = betterproto.which_one_of(obj[0], "threshold_type")[0]
        if not t:
            t = get_type_from_dict(obj[0])
        if t == 'auto_threshold':
            sat = SimpleAutoThreshold(
                type="AUTO",
                sensitivity=SimpleAutothresholdSensitivity.from_datawatch_object(obj[0].auto_threshold.sensitivity)
            )
            return sat
        elif t == 'constant_threshold':
            lower_bound = 0.0
            upper_bound = 0.0
            for i in obj:
                if i.constant_threshold.bound.bound_type == SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE:
                    lower_bound = i.constant_threshold.bound.value
                if i.constant_threshold.bound.bound_type == SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE:
                    upper_bound = i.constant_threshold.bound.value

            sct = SimpleConstantThreshold(type="CONSTANT", lower_bound=lower_bound, upper_bound=upper_bound)

            return sct
        elif t == 'relative_threshold':
            """Relative Threshold"""
            lower_bound = None
            upper_bound = None
            lookback = SimpleTimeInterval.from_datawatch_object(obj[0].relative_threshold.lookback)
            for i in obj:
                if i.relative_threshold.bound.bound_type == SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE:
                    lower_bound = i.relative_threshold.bound.value
                if i.relative_threshold.bound.bound_type == SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE:
                    upper_bound = i.relative_threshold.bound.value

            srt = SimpleRelativeThreshold(type="RELATIVE",
                                          lower_bound=lower_bound, upper_bound=upper_bound, lookback=lookback)

            return srt
        elif t == 'standard_deviation_threshold':
            """StdDev Threshold"""
            lower_bound = None
            upper_bound = None
            lookback = SimpleTimeInterval.from_datawatch_object(obj[0].standard_deviation_threshold.lookback)
            for i in obj:
                if i.standard_deviation_threshold.bound.bound_type == SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE:
                    lower_bound = i.standard_deviation_threshold.bound.value
                if i.standard_deviation_threshold.bound.bound_type == SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE:
                    upper_bound = i.standard_deviation_threshold.bound.value

            ssdt = SimpleStdDevThreshold(type="STDDEV",
                                         lower_bound=lower_bound, upper_bound=upper_bound, lookback=lookback)

            return ssdt
        elif t == 'freshness_schedule_threshold':
            """Freshness Schedule Threshold"""
            t = obj[0].freshness_schedule_threshold
            bound = t.bound.value
            dau = None if not t.delay_at_update else SimpleTimeInterval.from_datawatch_object(t.delay_at_update)
            ft = SimpleFreshnessThreshold(
                type='FRESHNESS',
                cron=t.cron, timezone=t.timezone, upper_bound=bound, delay_at_update=dau)
            return ft
        else:
            error_message = f"Threshold type not supported: {t}"
            raise InvalidConfigurationException(error_message)


class SimpleAutoThreshold(SimpleThreshold, type='AUTO'):
    sensitivity: SimpleAutothresholdSensitivity = SimpleAutothresholdSensitivity.MEDIUM
    upper_bound_only: bool = False

    def to_datawatch_object(self, **kwargs) -> List[Threshold]:
        lb = SimpleBound(bound_type=SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE, value=-1.0)
        ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=-1.0)
        mt = ForecastModelType.BOOTSTRAP_THRESHOLD_MODEL_TYPE
        s = self.sensitivity.to_datawatch_object()
        fv = -1.0

        lbat = AutoThreshold(
            bound=lb,
            model_type=mt,
            sensitivity=s,
            forecast_value=fv
        )
        ubat = AutoThreshold(
            bound=ub,
            model_type=mt,
            sensitivity=s,
            forecast_value=fv
        )
        if self.upper_bound_only:
            return [Threshold(auto_threshold=ubat)]
        else:
            return [Threshold(auto_threshold=lbat), Threshold(auto_threshold=ubat)]


class SimpleConstantThreshold(SimpleThreshold, type='CONSTANT'):
    upper_bound: Optional[float] = None
    lower_bound: Optional[float] = 0

    def to_datawatch_object(self) -> List[Threshold]:
        """
        Creates a list of protobuf Threshold objects from an instance of SimpleConstantThreshold
        :return: a List of Thresholds
        """
        thresholds: List[Threshold] = []
        if self.lower_bound:
            lb = SimpleBound(bound_type=SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE, value=self.lower_bound)
            lbt = Threshold(constant_threshold=ConstantThreshold(bound=lb))
            thresholds.append(lbt)
        if self.upper_bound:
            ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=self.upper_bound)
            ubt = Threshold(constant_threshold=ConstantThreshold(bound=ub))
            thresholds.append(ubt)

        return thresholds


class SimpleFreshnessThreshold(SimpleThreshold, type='FRESHNESS'):
    cron: str
    upper_bound: float
    timezone: Optional[str] = None
    delay_at_update: Optional[SimpleTimeInterval] = SimpleTimeInterval(interval_type=SimpleTimeIntervalType.HOURS,
                                                                       interval_value=0)

    def to_datawatch_object(self, **kwargs) -> List[Threshold]:
        thresholds: List[Threshold] = []
        ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=self.upper_bound)
        dau = self.delay_at_update.to_datawatch_object()
        ft = FreshnessScheduleThreshold(cron=self.cron, bound=ub, timezone=self.timezone, delay_at_update=dau)
        thresholds.append(Threshold(freshness_schedule_threshold=ft))

        return thresholds


class SimpleRelativeThreshold(SimpleThreshold, type='RELATIVE'):
    lookback: SimpleTimeInterval
    upper_bound: Optional[float] = None
    lower_bound: float = 0

    def to_datawatch_object(self, **kwargs) -> List[Threshold]:
        lkbk = self.lookback.to_datawatch_object()

        thresholds: List[Threshold] = []
        if self.lower_bound:
            lb = SimpleBound(bound_type=SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE, value=self.lower_bound)
            lbt = Threshold(relative_threshold=RelativeThreshold(lookback=lkbk, bound=lb))
            thresholds.append(lbt)
        if self.upper_bound:
            ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=self.upper_bound)
            ubt = Threshold(relative_threshold=RelativeThreshold(lookback=lkbk, bound=ub))
            thresholds.append(ubt)

        return thresholds


class SimpleStdDevThreshold(SimpleThreshold, type='STDDEV'):
    lookback: SimpleTimeInterval
    upper_bound: Optional[float] = None
    lower_bound: float = 0

    def to_datawatch_object(self, **kwargs) -> List[Threshold]:
        lkbk = self.lookback.to_datawatch_object()

        thresholds: List[Threshold] = []
        if self.lower_bound:
            lb = SimpleBound(bound_type=SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE, value=self.lower_bound)
            lbt = Threshold(standard_deviation_threshold=StandardDeviationThreshold(lookback=lkbk, bound=lb))
            thresholds.append(lbt)
        if self.upper_bound:
            ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=self.upper_bound)
            ubt = Threshold(standard_deviation_threshold=StandardDeviationThreshold(lookback=lkbk, bound=ub))
            thresholds.append(ubt)

        return thresholds


SNC = TypeVar('SNC', bound='SimpleNotificationChannel')


class SimpleNotificationChannel(PydanticSubtypeSerializable, DatawatchFacade, ABC):
    type: str

    @classmethod
    def from_datawatch_object(cls, obj: NotificationChannel) -> SNC:
        t = betterproto.which_one_of(obj, "notification_channel")[0]
        if not t:
            t = get_type_from_dict(obj)
        if t == 'email':
            return EmailNotificationChannel(type='EMAIL', value=obj.email)
        elif t == 'slack_channel':
            return SlackNotificationChannel(type='SLACK', value=obj.slack_channel)
        else:
            error_message = f"Notification channel type not supported: {t}"
            raise InvalidConfigurationException(error_message)


class EmailNotificationChannel(SimpleNotificationChannel, type='EMAIL'):
    value: str

    @validator('value')
    def must_have_correct_email_format(cls, v):
        p = re.compile(r'([A-Za-z0-9]+[.-_+])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(p, v):
            error_message = FORMATTING_ERRMSG.format(s=v)
            cls.register_validation_error(error_lines=[v],
                                          error_message=error_message)

        return v

    def to_datawatch_object(self, **kwargs) -> NotificationChannel:
        return NotificationChannel(email=self.value)


class SlackNotificationChannel(SimpleNotificationChannel, type='SLACK'):
    value: str

    @validator('value')
    def must_have_valid_channel_format(cls, v):
        p = re.compile(r'[#@]\S{1,20}')
        if not re.fullmatch(p, v):
            error_message = FORMATTING_ERRMSG.format(s=v)
            cls.register_validation_error(error_lines=[v],
                                          error_message=error_message)

        return v

    def to_datawatch_object(self, **kwargs) -> NotificationChannel:
        return NotificationChannel(slack_channel=self.value)


class SimpleMetricParameter(YamlModelWithValidatorContext, DatawatchFacade):
    key: str
    string_value: Optional[str] = None
    column_name: Optional[str] = None
    number_value: Optional[float] = None

    @classmethod
    def from_datawatch_object(cls, obj: MetricParameter) -> SimpleMetricParameter:
        return SimpleMetricParameter(key=obj.key,
                                     string_value=obj.string_value,
                                     column_name=obj.column_name,
                                     number_value=obj.number_value)

    def to_datawatch_object(self, **kwargs) -> MetricParameter:
        return MetricParameter(key=self.key,
                               string_value=self.string_value,
                               column_name=self.column_name,
                               number_value=self.number_value)


class SimpleSLA(YamlModelWithValidatorContext, DatawatchFacade):
    name: str
    id: int = None
    description: str = None
    metric_ids: List[int] = None
    notification_channels: List[SimpleNotificationChannel] = Field(default_factory=lambda: [])
    muted_until_timestamp: int = 0

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=SimpleSLA, attribute_name='metric_ids', values=values)
        must_be_list_validator(clazz=SimpleSLA, attribute_name='notification_channels', values=values)

        return values

    def merge_for_upsert(self, existing: SimpleSLA, overwrite: bool = True) -> SimpleSLA:
        """
        Merges this SLA and existing SLA.  Attributes that will be merged include: notificaiton channels and metric ids.

        If not overwriting: missing names, descriptions, and muted_until_timestamp will be populated with
        existing values.

        If overwriting: (current default strategy) new attributes will replace the old -- even if empty.

        Args:
            existing: the existing SLA to merge this new SLA with.
            overwrite: true/false

        Returns: The merged SLA

        """
        new_sla = self.copy(deep=True)

        # set existing SLA ID.
        new_sla.id = existing.id

        if not overwrite:
            """If we are not overwriting then we want to merge notifivation channels and metric ids."""
            if not new_sla.name:
                new_sla.name = existing.name

            if not new_sla.description:
                new_sla.description = existing.description

            if not new_sla.muted_until_timestamp:
                new_sla.muted_until_timestamp = existing.muted_until_timestamp

            if new_sla.notification_channels:
                new_sla.notification_channels.extend(existing.notification_channels)
            else:
                new_sla.notification_channels = existing.notification_channels

            if new_sla.metric_ids:
                new_sla.metric_ids.extend(existing.metric_ids)
            else:
                new_sla.metric_ids = existing.metric_ids

        return new_sla

    @classmethod
    def from_datawatch_object(cls, obj: Collection) -> SimpleSLA:
        sla = SimpleSLA(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            metric_ids=obj.metric_ids,
            muted_until_timestamp=obj.muted_until_timestamp
        )

        if obj.notification_channels:
            sla.notification_channels = [SimpleNotificationChannel.from_datawatch_object(nc)
                                         for nc in obj.notification_channels]

        return sla

    def to_datawatch_object(self) -> Collection:
        c = Collection(
            id=self.id,
            name=self.name,
            description=self.description if self.description else "SDK Generated.",
            metric_ids=self.metric_ids,
            notification_channels=[nc.to_datawatch_object() for nc in self.notification_channels],
            muted_until_timestamp=self.muted_until_timestamp
        )

        return c


class BucketSize(YamlStrEnum):
    DAY = "DAY"  # 86400
    HOUR = "HOUR"  # 3600

    def to_seconds(self):
        if self == BucketSize.DAY:
            return 86400
        elif self == BucketSize.HOUR:
            return 3600
        else:
            return 86400  # defaults to day.

    @classmethod
    def from_seconds(cls, seconds: int) -> Union[int, BucketSize]:
        if seconds == 86400:
            return BucketSize.DAY
        elif seconds == 3600:
            return BucketSize.HOUR
        else:
            return seconds


class SimpleLookback(YamlModelWithValidatorContext):
    lookback_window: Optional[SimpleTimeInterval] = SimpleTimeInterval(interval_type=SimpleTimeIntervalType.DAYS,
                                                                       interval_value=2)
    lookback_type: Optional[SimpleLookbackType] = SimpleLookbackType.DATA_TIME
    bucket_size: Optional[Union[int, BucketSize]] = BucketSize.DAY


class SimpleMetricDefinition(YamlModelWithValidatorContext, DatawatchFacade):
    saved_metric_id: Optional[str] = None
    metric_type: SimpleMetricType = None
    metric_name: Optional[str] = None
    description: Optional[str] = None
    schedule_frequency: Optional[SimpleTimeInterval] = None
    conditions: Optional[List[str]] = None
    group_by: Optional[List[str]] = None
    threshold: Optional[SimpleThreshold] = None
    notification_channels: Optional[List[SimpleNotificationChannel]] = None
    parameters: Optional[List[SimpleMetricParameter]] = None
    lookback: Optional[SimpleLookback] = SimpleLookback()
    muted_until_epoch_seconds: Optional[int] = 0
    sla_ids: Optional[List[int]] = Field(default_factory=lambda: [])

    @validator('threshold', always=True, pre=False)
    def set_default_threshold(cls, threshold, values):
        metric_type = values['metric_type']

        if threshold:
            """For the case that a user has specifically defined a metric"""
            return threshold
        elif not metric_type:
            """For the case where this is a saved metric reference."""
            return threshold
        elif metric_type \
                and metric_type.type == 'PREDEFINED' \
                and metric_type in SimpleMetricType.get_freshness_metric_types() \
                and not threshold:
            """Standard is that freshness thresholds always are medium autothresholds with upper bound only."""
            threshold = SimpleAutoThreshold(type='AUTO',
                                            sensitivity=SimpleAutothresholdSensitivity.MEDIUM,
                                            upper_bound_only=True
                                            )
        else:
            """otherwise, if no threshold entered, then should default to a medium autothreshold with upper and
            lower bounds."""
            threshold = SimpleAutoThreshold(type='AUTO',
                                            sensitivity=SimpleAutothresholdSensitivity.MEDIUM,
                                            upper_bound_only=False)

        return threshold

    @validator('schedule_frequency', always=True, pre=False)
    def set_default_schedule_frequency(cls, schedule_frequency, values):
        metric_type = values['metric_type']

        if schedule_frequency:
            """For the case that a user has specifically defined a metric"""
            return schedule_frequency
        elif not metric_type:
            """For the case where this is a saved metric reference."""
            return schedule_frequency
        elif metric_type \
                and metric_type in SimpleMetricType.get_freshness_metric_types():
            """Freshness metrics should execute every 6 hours by default WIZ-1623"""
            return SimpleTimeInterval(interval_type=SimpleTimeIntervalType.HOURS, interval_value=6)
        else:
            """All other metrics should execute every 24 hours by default WIZ-1623"""
            return SimpleTimeInterval(interval_type=SimpleTimeIntervalType.HOURS, interval_value=24)

    def get_error_lines(self) -> List[str]:
        """
        Override from super.  Returns object serialized to yaml and split to lines.  Used to search files.  If this is
        a saved metric, it returns the saved_metric_id dict because that is what the original file would have contained.
        Otherwise, it returns a full object as string broken down by lines.
        Returns: List of yaml string lines.

        """
        if self.saved_metric_id:
            return safe_split_dict_entry_lines('saved_metric_id', self.saved_metric_id)
        else:
            return self.yaml(exclude_unset=True, exclude_defaults=True,
                             exclude_none=True, indent=True).splitlines()

    @validator('metric_type', pre=True)
    def must_be_dict_type(cls, metric_type):
        if isinstance(metric_type, SimplePredefinedMetric):
            return metric_type

        if metric_type and not isinstance(metric_type, dict):
            errlns = yaml.safe_dump({'metric_type': metric_type}, indent=True, sort_keys=False)
            SimpleMetricDefinition.register_validation_error(
                error_lines=[errlns],
                error_message=FORMATTING_ERRMSG.format(
                    s='Metric Type is an object.  Please include `type` and `metric` attributes')
            )

            return {'type': 'PREDEFINED', 'metric': 'UNDEFINED'}

        return metric_type

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=SimpleMetricDefinition, attribute_name='sla_ids', values=values)
        must_be_list_validator(clazz=SimpleMetricDefinition, attribute_name='conditions', values=values)
        must_be_list_validator(clazz=SimpleMetricDefinition, attribute_name='group_by', values=values)
        must_be_list_validator(clazz=SimpleMetricDefinition, attribute_name='parameters', values=values)

        return values

    def deployment_validations(self, config_error_lines: List[str]):
        """
        Runs all deployment validations for SimpleMetricDefinitions
        Args:
            config_error_lines: The congiruation serialized to yaml and split to lines.

        Returns: None
        """
        self.deployments_must_have_metric_type_if_not_saved_metric_id(config_error_lines=config_error_lines)
        self.deployments_cannot_have_metric_type_if_has_saved_metric_id(config_error_lines=config_error_lines)

    def deployments_must_have_metric_type_if_not_saved_metric_id(self, config_error_lines: List[str]):
        """
        Metric definitions must have a metric type if not referencing a saved metric by id
        (deployment in-line metrics)
        Args:
            config_error_lines: The congiruation serialized to yaml and split to lines.

        Returns: None
        """
        if not self.saved_metric_id and not self.metric_type:
            error_message = MUST_HAVE_METRIC_TYPE_ERRMSG.format(config_error_lines=config_error_lines)
            self.register_validation_error(error_lines=self.get_error_lines(),
                                           error_context_lines=config_error_lines,
                                           error_message=error_message)

    def deployments_cannot_have_metric_type_if_has_saved_metric_id(self, config_error_lines: List[str]):
        """Metric definitions cannot have a metric_ type if referencing a saved_metric_id but no metric_type
            (deployment reference of saved metric)
        Args:
            config_error_lines: The congiruation serialized to yaml and split to lines.

        Returns: None
        """
        if self.saved_metric_id and self.metric_type:
            error_message = OVERRIDE_METRIC_TYPE_SAVED_METRIC_ERRMSG.format(config_error_lines=config_error_lines)
            self.register_validation_error(error_lines=self.get_error_lines(),
                                           error_context_lines=config_error_lines,
                                           error_message=error_message)

    def saved_metrics_must_have_id(self, config_error_lines: List[str]):
        """
        Saved Metric Definitions must have a saved metric id.
        Args:
            config_error_lines: The congiruation serialized to yaml and split to lines.

        Returns: None
        """
        if not self.saved_metric_id:
            error_mesage = MUST_HAVE_METRIC_ID_ERRMSG.format(config_error_lines=config_error_lines)
            self.register_validation_error(error_lines=self.get_error_lines(),
                                           error_context_lines=config_error_lines,
                                           error_message=error_mesage)

    @classmethod
    def from_datawatch_object(cls, obj: Union[MetricDefinition, MetricConfiguration]) -> SimpleMetricDefinition:
        builder = SimpleMetricDefinition()
        builder.metric_type = SimpleMetricType.from_datawatch_object(obj.metric_type)
        builder.metric_name = obj.name
        builder.description = obj.description

        builder.schedule_frequency = SimpleTimeInterval.from_datawatch_object(obj.schedule_frequency)

        builder.conditions = obj.filters
        builder.group_by = obj.group_bys

        builder.threshold = SimpleThreshold.from_datawatch_object(obj.thresholds)

        builder.notification_channels = [SimpleNotificationChannel.from_datawatch_object(nc)
                                         for nc in obj.notification_channels]

        builder.parameters = [SimpleMetricParameter.from_datawatch_object(p) for p in obj.parameters]

        builder.lookback = SimpleLookback(lookback_window=SimpleTimeInterval.from_datawatch_object(obj.lookback),
                                          lookback_type=SimpleLookbackType.from_datawatch_object(obj.lookback_type),
                                          bucket_size=BucketSize.from_seconds(obj.grain_seconds))

        builder.muted_until_epoch_seconds = obj.muted_until_epoch_seconds

        builder.sla_ids = obj.collection_ids

        return builder

    def to_datawatch_object(self, **kwargs) -> MetricDefinition:
        builder = MetricDefinition()

        # Verifying that metric_type has been set before serializing to datawatch object.
        if self.metric_type:
            builder.metric_type = self.metric_type.to_datawatch_object()
        else:
            InvalidConfigurationException(
                "Metric Type cannot be None.  Verify that Saved Metric IDs have been applied.")

        builder.name = self.metric_name
        builder.description = self.description

        if self.schedule_frequency:
            builder.schedule_frequency = self.schedule_frequency.to_datawatch_object()

        builder.filters = self.conditions
        builder.group_bys = self.group_by

        if self.threshold:
            builder.thresholds = self.threshold.to_datawatch_object()

        if self.notification_channels:
            builder.notification_channels = [nc.to_datawatch_object() for nc in self.notification_channels]

        if self.parameters:
            builder.parameters = [p.to_datawatch_object() for p in self.parameters]

        if self.lookback:
            if self.lookback.lookback_window:
                builder.lookback = self.lookback.lookback_window.to_datawatch_object()

            if self.lookback.lookback_type:
                builder.lookback_type = self.lookback.lookback_type.to_datawatch_object()

            builder.grain_seconds = self.lookback.bucket_size.to_seconds()

        builder.muted_until_epoch_seconds = self.muted_until_epoch_seconds

        if self.sla_ids:
            builder.collection_ids = self.sla_ids

        return builder
