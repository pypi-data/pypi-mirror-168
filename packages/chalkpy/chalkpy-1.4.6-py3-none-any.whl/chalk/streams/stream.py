import dataclasses
import inspect
from typing import Any, Callable, List, Optional, Union

from chalk.features.resolver import MachineType
from chalk.streams.StreamSource import StreamSource
from chalk.streams.StreamUpdate import StreamUpdate


class StreamResolver:
    registry = []

    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        source: StreamSource,
        fn: Callable,
        environment: Optional[Union[List[str], str]],
        machine_type: Optional[MachineType],
    ):
        super(StreamResolver, self).__init__()
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.source = source
        self.fn = fn
        self.environment = environment
        self.doc = doc
        self.machine_type = machine_type

    def __eq__(self, other):
        return isinstance(other, StreamResolver) and self.fqn == other.fqn

    def __hash__(self):
        return hash(self.fqn)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __repr__(self):
        return f"StreamResolver(name={self.fqn})"


@dataclasses.dataclass
class StreamResolverParseResult:
    fqn: str
    source: StreamSource
    function_definition: str
    function: Callable
    doc: Optional[str]


def _parse_function(fn: Callable) -> StreamResolverParseResult:
    fqn = f"{fn.__module__}.{fn.__name__}"
    sig = inspect.signature(fn)

    function_definition = inspect.getsource(fn)

    if len(sig.parameters.values()) != 1:
        raise ValueError(f"Expected exactly one parameter for stream: {fqn}")

    arg = list(sig.parameters.values())[0].annotation

    return StreamResolverParseResult(
        fqn=fqn,
        source=arg,
        function_definition=function_definition,
        function=fn,
        doc=fn.__doc__,
    )


def stream(
    fn: Optional[Callable[[Any], StreamUpdate]] = None,
    environment: Optional[Union[List[str], str]] = None,
    machine_type: Optional[MachineType] = None,
):
    caller_filename = inspect.stack()[1].filename

    def decorator(args, cf=caller_filename):
        parsed = _parse_function(args)

        resolver = StreamResolver(
            filename=cf,
            source=parsed.source,
            function_definition=parsed.function_definition,
            fqn=parsed.fqn,
            doc=fn.__doc__,
            fn=parsed.function,
            environment=environment,
            machine_type=machine_type,
        )
        StreamResolver.registry.append(resolver)
        return resolver

    return decorator(fn) if fn else decorator
