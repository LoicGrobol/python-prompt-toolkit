"""
Dummy contextvars implementation, to make prompt_toolkit work on Python 3.6.

As long as there is only one application running at a time, we don't need the
real contextvars. So, stuff like the telnet-server and so on requires 3.7.
"""
from typing import TYPE_CHECKING, Callable, Generic, Optional, TypeVar

if TYPE_CHECKING:
    from typing_extensions import ParamSpec


def copy_context() -> "Context":
    return Context()


if TYPE_CHECKING:
    _P = ParamSpec("_P")
_T = TypeVar("_T")


class Context:
    def run(
        self, callable: "Callable[_P, _T]", *args: "_P.args", **kwargs: "_P.kwargs"
    ) -> _T:
        return callable(*args, **kwargs)

    def copy(self) -> "Context":
        return self


class Token(Generic[_T]):
    pass


class ContextVar(Generic[_T]):
    def __init__(self, name: str, *, default: Optional[_T] = None) -> None:
        self._name = name
        self._value = default

    @property
    def name(self) -> str:
        return self._name

    def get(self, default: Optional[_T] = None) -> _T:
        result = self._value or default
        if result is None:
            raise LookupError
        return result

    def set(self, value: _T) -> Token[_T]:
        self._value = value
        return Token()

    def reset(self, token: Token[_T]) -> None:
        pass
