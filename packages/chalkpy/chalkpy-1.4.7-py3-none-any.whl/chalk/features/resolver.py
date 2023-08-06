import dataclasses
import inspect
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Protocol, Type, Union, get_type_hints

from chalk.features import DataFrame
from chalk.features.feature import Feature, Features, FeatureWrapper, Filter
from chalk.features.tag import Environments, Tags
from chalk.sql.base.protocols import BaseSQLSourceProtocol
from chalk.utils.duration import Duration, ScheduleOptions

MachineType = str


class FilterFunction(Protocol):
    def __call__(self, *args: Feature) -> bool:
        ...


class SampleFunction(Protocol):
    def __call__(self) -> Features:
        ...


@dataclass
class Cron:
    schedule: Optional[ScheduleOptions] = None
    filter: Optional[FilterFunction] = None
    sample: Optional[SampleFunction] = None


class Resolver(Protocol):
    function_definition: str
    fqn: str
    filename: str
    inputs: List[Feature]
    output: Type[Features]
    fn: Callable
    environment: Optional[Environments]
    tags: Optional[Tags]
    max_staleness: Optional[Duration]
    machine_type: Optional[MachineType]

    registry: "List[Resolver]" = []

    def __hash__(self):
        return hash(self.fqn)


def _process_call(result):
    from chalk.sql.integrations.chalk_query import ChalkQuery, StringChalkQuery

    if isinstance(result, (ChalkQuery, StringChalkQuery)):
        return result.execute()

    return result


class SinkResolver:
    registry: "List[SinkResolver]" = []

    def __eq__(self, other):
        return isinstance(other, SinkResolver) and self.fqn == other.fqn

    def __hash__(self):
        return hash(self.fqn)

    def __call__(self, *args, **kwargs):
        return _process_call(self.fn(*args, **kwargs))

    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        inputs: List[Feature],
        output: Features,
        fn: Callable,
        environment: Optional[Environments],
        tags: Optional[Tags],
        machine_type: Optional[MachineType],
        buffer_size: Optional[int],
        debounce: Optional[Duration],
        max_delay: Optional[Duration],
        upsert: Optional[bool],
        integration: Optional[BaseSQLSourceProtocol] = None,
    ):
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.inputs = inputs
        self.output = output
        self.fn = fn
        self.environment = environment
        self.tags = tags
        self.doc = doc
        self.machine_type = machine_type
        self.buffer_size = buffer_size
        self.debounce = debounce
        self.max_delay = max_delay
        self.upsert = upsert
        self.integration = integration

    def __repr__(self):
        return f"SinkResolver(name={self.fqn})"


class OnlineResolver(Resolver):
    cron: Union[ScheduleOptions, Cron]

    def __eq__(self, other):
        return isinstance(other, OnlineResolver) and self.fqn == other.fqn

    def __hash__(self):
        return hash(self.fqn)

    def __call__(self, *args, **kwargs):
        return _process_call(self.fn(*args, **kwargs))

    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        inputs: List[Feature],
        output: Type[Features],
        fn: Callable,
        environment: Optional[Environments],
        tags: Optional[Tags],
        max_staleness: Optional[Duration],
        cron: Optional[Union[ScheduleOptions, Cron]],
        machine_type: Optional[MachineType],
        when: Optional[Filter],
    ):
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.inputs = inputs
        self.output = output
        self.fn = fn
        self.environment = environment
        self.tags = tags
        self.max_staleness = max_staleness
        self.cron = cron
        self.doc = doc
        self.machine_type = machine_type
        self.when = when

    def __repr__(self):
        return f"OnlineResolver(name={self.fqn})"


class OfflineResolver(Resolver):
    def __eq__(self, other):
        return isinstance(other, OfflineResolver) and self.fqn == other.fqn

    def __hash__(self):
        return hash(self.fqn)

    def __call__(self, *args, **kwargs):
        return _process_call(self.fn(*args, **kwargs))

    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        inputs: List[Feature],
        output: Type[Features],
        fn: Callable,
        environment: Optional[Environments],
        tags: Optional[Tags],
        max_staleness: Optional[Duration],
        cron: Union[ScheduleOptions, Cron],
        machine_type: Optional[MachineType],
    ):
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.doc = doc
        self.inputs = inputs
        self.output = output
        self.fn = fn
        self.environment = environment
        self.tags = tags
        self.max_staleness = max_staleness
        self.cron = cron
        self.machine_type = machine_type

    def __repr__(self):
        return f"OfflineResolver(name={self.fqn})"


@dataclasses.dataclass
class ResolverParseResult:
    fqn: str
    inputs: List[Feature]
    output: Optional[Type[Features]]
    function_definition: str
    function: Callable
    doc: Optional[str]


def parse_function(fn: Callable, ignore_return: bool = False) -> ResolverParseResult:
    fqn = f"{fn.__module__}.{fn.__name__}"
    sig = inspect.signature(fn)

    function_definition = inspect.getsource(fn)
    return_annotation = get_type_hints(fn)["return"]

    ret_val = None

    if isinstance(return_annotation, FeatureWrapper):
        return_annotation = return_annotation._chalk_feature

    if isinstance(return_annotation, Feature):
        assert return_annotation.typ is not None

        if return_annotation.is_has_many:
            assert issubclass(return_annotation.typ.parsed_annotation, DataFrame)
            ret_val = Features[return_annotation.typ.parsed_annotation.columns]
        elif return_annotation.is_has_one:
            assert issubclass(return_annotation.typ.underlying, Features)
            ret_val = Features[return_annotation.typ.underlying.features]
        else:
            # function annotated like def get_account_id(user_id: User.id) -> User.account_id
            ret_val = Features[return_annotation]

    if ret_val is None:
        if not isinstance(return_annotation, type):
            raise TypeError(f"return_annotation {return_annotation} of type {type(return_annotation)} is not a type")
        if issubclass(return_annotation, Features):
            # function annotated like def get_account_id(user_id: User.id) -> Features[User.account_id]
            # or def get_account_id(user_id: User.id) -> User:
            ret_val = return_annotation
        elif issubclass(return_annotation, DataFrame):
            # function annotated like def get_transactions(account_id: Account.id) -> DataFrame[Transaction]
            ret_val = Features[return_annotation]

    if ret_val is None and not ignore_return:
        raise ValueError(f"Resolver {fqn} did not have a valid return type")

    inputs = [p.annotation for p in sig.parameters.values()]

    # Unwrap anything that is wrapped with FeatureWrapper
    inputs = [p._chalk_feature if isinstance(p, FeatureWrapper) else p for p in inputs]

    return ResolverParseResult(
        fqn=fqn,
        inputs=inputs,
        output=ret_val,
        function_definition=function_definition,
        function=fn,
        doc=fn.__doc__,
    )


def online(
    fn: Optional[Callable] = None,
    /,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: Optional[Union[ScheduleOptions, Cron]] = None,
    machine_type: Optional[MachineType] = None,
    when: Optional[Any] = None,
):
    caller_filename = inspect.stack()[1].filename

    def decorator(args, cf=caller_filename):
        parsed = parse_function(args)
        if parsed.fqn in {s.fqn for s in Resolver.registry}:
            raise ValueError(f"Duplicate resolver {parsed.fqn}")
        Resolver.registry.append(
            OnlineResolver(
                filename=cf,
                function_definition=parsed.function_definition,
                fqn=parsed.fqn,
                doc=parsed.doc,
                inputs=parsed.inputs,
                output=parsed.output,
                fn=parsed.function,
                environment=environment,
                tags=tags,
                max_staleness=None,
                cron=cron,
                machine_type=machine_type,
                when=when,
            )
        )
        return args

    return decorator(fn) if fn else decorator


def offline(
    fn: Optional[Callable] = None,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: Union[ScheduleOptions, Cron] = None,
    machine_type: Optional[MachineType] = None,
):
    caller_filename = inspect.stack()[1].filename

    def decorator(args, cf=caller_filename):
        parsed = parse_function(args)
        if parsed.fqn in {s.fqn for s in Resolver.registry}:
            raise ValueError(f"Duplicate resolver {parsed.fqn}")
        Resolver.registry.append(
            OfflineResolver(
                filename=cf,
                function_definition=parsed.function_definition,
                fqn=parsed.fqn,
                doc=parsed.doc,
                inputs=parsed.inputs,
                output=parsed.output,
                fn=parsed.function,
                environment=environment,
                tags=tags,
                max_staleness=None,
                cron=cron,
                machine_type=machine_type,
            )
        )
        return args

    return decorator(fn) if fn else decorator


def sink(
    fn: Optional[Callable] = None,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    machine_type: Optional[MachineType] = None,
    buffer_size: Optional[int] = None,
    debounce: Optional[Duration] = None,
    max_delay: Optional[Duration] = None,
    upsert: Optional[bool] = None,
    integration: Optional[BaseSQLSourceProtocol] = None,
):
    caller_filename = inspect.stack()[1].filename

    def decorator(args, cf=caller_filename):
        parsed = parse_function(args, ignore_return=True)
        SinkResolver.registry.append(
            SinkResolver(
                filename=cf,
                function_definition=parsed.function_definition,
                fqn=parsed.fqn,
                doc=parsed.doc,
                inputs=parsed.inputs,
                output=parsed.output,
                fn=parsed.function,
                environment=environment,
                tags=tags,
                machine_type=machine_type,
                buffer_size=buffer_size,
                debounce=debounce,
                max_delay=max_delay,
                upsert=upsert,
                integration=integration,
            )
        )
        return args

    return decorator(fn) if fn else decorator
