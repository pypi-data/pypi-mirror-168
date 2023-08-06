from dataclasses import dataclass
from datetime import datetime
from operator import attrgetter

from bigeye_sdk.generated.com.torodata.models.generated import MetricInfo, MetricRun, SimpleBoundType


@dataclass
class UpperLower:
    upper: float = 0.0
    lower: float = 0.0


def get_most_recent_run(metric_info: MetricInfo) -> MetricRun:
    return max(metric_info.latest_metric_runs, key=attrgetter('run_at_epoch_seconds'))


def get_most_recent_run_time(most_recent_run: MetricRun) -> str:
    return datetime.fromtimestamp(most_recent_run.run_at_epoch_seconds).strftime('%Y-%m-%d %H:%M:%S')


def get_upper_lower_thresholds(most_recent_run: MetricRun) -> UpperLower:
    ul = UpperLower()

    for t in most_recent_run.thresholds:
        if t.bound.bound_type == SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE:
            ul.upper = t.bound.value
        elif t.bound.bound_type == SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE:
            ul.lower = t.bound.value

    return ul