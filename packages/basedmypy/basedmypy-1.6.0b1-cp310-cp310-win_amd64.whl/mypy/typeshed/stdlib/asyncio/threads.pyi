from collections.abc import Callable
from typing import TypeVar
from typing_extensions import ParamSpec

__all__ = ("to_thread",)
_P = ParamSpec("_P")
_R = TypeVar("_R")

async def to_thread(__func: Callable[_P, _R], *args: _P.args, **kwargs: _P.kwargs) -> _R: ...
