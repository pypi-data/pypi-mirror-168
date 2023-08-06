import builtins
import types
from typing import Any, List, Mapping, Optional, Type


# A sentinel object to detect if a parameter is supplied or not.
# Use a class to give it a better repr.
class _MISSING_TYPE:
    def __repr__(self):
        return "<MISSING>"


MISSING = _MISSING_TYPE()


def create_fn(
    name: str,
    args: List[str],
    body: List[str],
    *,
    _globals: Optional[Mapping[str, Any]] = None,
    _locals: Optional[Mapping[str, Any]] = None,
    return_type: Any = MISSING,
):
    # Note that we mutate locals when exec() is called.  Caller
    # beware!  The only callers are internal to this module, so no
    # worries about external callers.
    if _locals is None:
        _locals = {}
    if "BUILTINS" not in _locals:
        _locals["BUILTINS"] = builtins
    return_annotation = ""
    if return_type is not MISSING:
        _locals["_return_type"] = return_type
        return_annotation = "->_return_type"
    body_text = "\n".join(f"  {b}" for b in body)

    # Compute the text of the entire function.
    txt = f' def {name}({",".join(args)}){return_annotation}:\n{body_text}'

    local_vars = ", ".join(_locals.keys())
    txt = f"def __create_fn__({local_vars}):\n{txt}\n return {name}"
    ns: Mapping[str, Any] = {}
    exec(txt, _globals, ns)
    return ns["__create_fn__"](**_locals)


def _set_qualname(cls, value):
    # Ensure that the functions returned from _create_fn uses the proper
    # __qualname__ (the class they belong to).
    if isinstance(value, types.FunctionType):
        value.__qualname__ = f"{cls.__qualname__}.{value.__name__}"
    return value


def set_new_attribute(cls: Type, name: str, value: Any):
    # Never overwrites an existing attribute.  Returns True if the
    # attribute already exists.
    if name in cls.__dict__:
        return True
    _set_qualname(cls, value)
    setattr(cls, name, value)
    return False


def field_assign(name: str, value: str, self_name: str):
    # self_name is what "self" is called in this function: don't
    # hard-code "self", since that might be a field name.
    return f"{self_name}.{name}={value}"
