import inspect
import logging
from typing import Callable, List, Optional, Set, TypeVar, Union, overload

T = TypeVar("T")


HookFn = Callable[[], T]
EnvironmentFilter = Optional[Union[List[str], str]]


def _run_all_hooks(environment: str, hooks: Set["Hook"]) -> None:
    relevant = [h for h in hooks if h.environment is not None and environment in h.environment]
    for hook in relevant:
        try:
            hook()
        except Exception as e:
            logging.error(f"Error running hook {hook.fn.__name__}")
            raise e


class Hook:
    # Registry
    before_all: Set["Hook"] = set()
    after_all: Set["Hook"] = set()

    environment: Optional[List[str]]
    fn: HookFn
    filename: str

    def __init__(self, fn: HookFn, filename: str, environment: Optional[EnvironmentFilter] = None):
        self.fn = fn
        self.filename = filename
        self.environment = (
            [
                environment,
            ]
            if isinstance(environment, str)
            else environment
        )

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __repr__(self):
        return f'Hook(filename={self.filename}, fn={self.fn.__name__}", environment={str(self.environment)})'

    @classmethod
    def run_all_before_all(cls, environment: str) -> None:
        return _run_all_hooks(environment, cls.before_all)

    @classmethod
    def run_all_after_all(cls, environment: str) -> None:
        return _run_all_hooks(environment, cls.after_all)


@overload
def before_all(fn: HookFn, /) -> Hook:
    ...


@overload
def before_all(fn: None = None, /, environment: EnvironmentFilter = None) -> Callable[[HookFn], Hook]:
    ...


def before_all(
    fn: Optional[HookFn] = None, /, environment: EnvironmentFilter = None
) -> Union[Hook, Callable[[HookFn], Hook]]:
    caller_filename = inspect.stack()[1].filename

    def decorator(f, cf=caller_filename):
        hook = Hook(fn=f, filename=cf, environment=environment)
        Hook.before_all.add(hook)
        return hook

    return decorator(fn) if fn else decorator


@overload
def after_all(fn: HookFn, /, environment: EnvironmentFilter = None) -> Hook:
    ...


@overload
def after_all(fn: None = None, /, environment: EnvironmentFilter = None) -> Callable[[HookFn], Hook]:
    ...


def after_all(
    fn: Optional[HookFn] = None, /, environment: EnvironmentFilter = None
) -> Union[Hook, Callable[[HookFn], Hook]]:
    caller_filename = inspect.stack()[1].filename

    def decorator(f, cf=caller_filename):
        hook = Hook(fn=f, filename=cf, environment=environment)
        Hook.after_all.add(hook)
        return hook

    return decorator(fn) if fn else decorator
