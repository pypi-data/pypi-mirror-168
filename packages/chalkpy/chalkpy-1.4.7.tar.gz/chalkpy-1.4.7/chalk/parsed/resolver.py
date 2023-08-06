from dataclasses import dataclass
from typing import Callable, List, Optional, Protocol, Sequence, TypeVar, Union

from chalk.features.resolver import Cron, FilterFunction, MachineType
from chalk.parsed.feature import FeatureSetType, FeatureType, FilterParsed, QueryInputType
from chalk.utils.collections import get_unique_item
from chalk.utils.duration import Duration, ScheduleOptions

T = TypeVar("T")


@dataclass
class CronFilterWithFeatureArgs:
    filter: FilterFunction
    feature_args: List[FeatureType]


class ResolverParsed(Protocol):
    function_definition: str
    filename: str
    fqn: str
    doc: Optional[str]
    inputs: Sequence[QueryInputType]
    output: FeatureSetType
    raw_fn: Callable
    fn: Callable
    environment: Optional[List[str]]
    tags: Optional[List[str]]
    machine_type: Optional[MachineType]
    when: Optional[FilterParsed]

    registry: "List[ResolverParsed]" = []

    def short_name(self) -> str:
        return self.fqn.split(".")[-1]

    def __hash__(self):
        return hash(self.fqn)

    @property
    def root_ns(self):
        """The @features cls namespace for which this resolver is rooted."""
        return get_unique_item([x.root_namespace() for x in self.inputs], name="root namespace")


class OnlineResolverParsed(ResolverParsed):
    cron: Union[ScheduleOptions, Cron]

    def __eq__(self, other):
        return isinstance(other, OnlineResolverParsed) and self.fqn == other.fqn

    def __hash__(self):
        return hash(self.fqn)

    def __init__(
        self,
        function_definition: str,
        filename: str,
        fqn: str,
        doc: Optional[str],
        inputs: List[QueryInputType],
        output: FeatureSetType,
        raw_fn: Callable,
        fn: Callable,
        environment: Optional[List[str]],
        tags: Optional[List[str]],
        cron: Union[ScheduleOptions, Cron],
        cron_filter: Optional[CronFilterWithFeatureArgs],
        machine_type: Optional[MachineType],
        when: Optional[FilterParsed],
    ):
        super(OnlineResolverParsed, self).__init__()
        self.filename = filename
        self.function_definition = function_definition
        self.fqn = fqn
        self.inputs = inputs
        self.output = output
        self.fn = fn
        self.raw_fn = raw_fn
        self.environment = environment
        self.tags = tags
        self.cron = cron
        self.cron_filter = cron_filter
        self.doc = doc
        self.machine_type = machine_type
        self.when = when

    def __repr__(self):
        return f"""OnlineResolverParsed(
  name={self.fqn},
  inputs={self.inputs}
  output={self.output}
)"""


class SinkResolverParsed:
    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        inputs: List[FeatureType],
        raw_fn: Callable,
        environment: Optional[List[str]],
        tags: Optional[List[str]],
        machine_type: Optional[MachineType],
        buffer_size: Optional[int],
        debounce: Optional[Duration],
        max_delay: Optional[Duration],
        upsert: Optional[bool],
    ):
        self.filename = filename
        self.function_definition = function_definition
        self.fqn = fqn
        self.inputs = inputs
        self.raw_fn = raw_fn
        self.environment = environment
        self.tags = tags
        self.doc = doc
        self.machine_type = machine_type
        self.buffer_size = buffer_size
        self.debounce = debounce
        self.max_delay = max_delay
        self.upsert = upsert

    def __repr__(self):
        return f"""SinkResolverParsed(
  name={self.fqn},
  inputs={self.inputs}
)"""

    def __eq__(self, other):
        return isinstance(other, SinkResolverParsed) and self.fqn == other.fqn

    def __hash__(self):
        return hash(self.fqn)


class OfflineResolverParsed(ResolverParsed):
    def __eq__(self, other):
        return isinstance(other, OfflineResolverParsed) and self.fqn == other.fqn

    def __hash__(self):
        return hash(self.fqn)

    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        inputs: List[QueryInputType],
        output: FeatureSetType,
        raw_fn: Callable,
        fn: Callable,
        environment: Optional[List[str]],
        tags: Optional[List[str]],
        cron: Union[ScheduleOptions, Cron],
        cron_filter: Optional[CronFilterWithFeatureArgs],
        machine_type: Optional[MachineType],
    ):
        self.filename = filename
        self.function_definition = function_definition
        self.fqn = fqn
        self.inputs = inputs
        self.output = output
        self.fn = fn
        self.raw_fn = raw_fn
        self.environment = environment
        self.tags = tags
        self.cron = cron
        self.cron_filter = cron_filter
        self.doc = doc
        self.machine_type = machine_type
        self.when = None

    def __repr__(self):
        return f"""OfflineResolverParsed(
  name={self.fqn},
  inputs={self.inputs}
  output={self.output}
)"""
