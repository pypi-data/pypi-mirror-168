import collections.abc
from typing import Any, Dict, Generator, List, Optional, Sequence, Set, TypeVar, Union

T = TypeVar("T")


def flatten(v: Sequence[Union[T, Sequence[Union[T, Sequence[T]]]]]) -> List[T]:
    ret = []
    for x in v:
        if isinstance(x, collections.abc.Sequence) and not isinstance(x, (str, bytes, bytearray)):
            ret.extend(flatten(x))
        else:
            ret.append(x)
    return ret


def chunks(lst: Sequence[T], n: int) -> Generator[Sequence[T], None, None]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def ensure_tuple(x: Union[T, Sequence[T], Dict[Any, T], None]):
    """Converts ``x`` into a tuple.
    * If ``x`` is ``None``, then ``tuple()`` is returned.
    * If ``x`` is a tuple, then ``x`` is returned as-is.
    * If ``x`` is a list, then ``tuple(x)`` is returned.
    * If ``x`` is a dict, then ``tuple(v for v in x.values())`` is returned.
    Otherwise, a single element tuple of ``(x,)`` is returned.
    Args:
        x (Any): The input to convert into a tuple.
    Returns:
        tuple: A tuple of ``x``.
    """
    # From https://github.com/mosaicml/composer/blob/020ca02e3848ee8fb6b7fff0c8123f597b05be8a/composer/utils/iter_helpers.py#L40
    if x is None:
        return ()
    if isinstance(x, (str, bytes, bytearray)):
        return (x,)
    if isinstance(x, collections.abc.Sequence):
        return tuple(x)
    if isinstance(x, dict):
        return tuple(x.values())
    return (x,)


def flatten_sets(v: List[Set[T]]) -> Set[T]:
    return set().union(*v)


def get_unique_item(collection: Sequence[Optional[T]], name: str) -> T:
    item = None
    for x in collection:
        if x is None:
            raise ValueError(f"Item in {name} is None")
        if item is not None:
            if x != item:
                raise ValueError(f"Multiple values in {name} are not permitted. Found {x}, {item}")
        item = x
    if item is None:
        raise ValueError(f"There should be at least one item in {name}")
    return item
