from collections.abc import Callable, Sequence
from contextvars import Context
from typing import Any
from typing_extensions import Literal

from . import futures

__all__ = ()

# asyncio defines 'isfuture()' in base_futures.py and re-imports it in futures.py
# but it leads to circular import error in pytype tool.
# That's why the import order is reversed.
from .futures import isfuture as isfuture

_PENDING: Literal["PENDING"]  # undocumented
_CANCELLED: Literal["CANCELLED"]  # undocumented
_FINISHED: Literal["FINISHED"]  # undocumented

def _format_callbacks(cb: Sequence[tuple[Callable[[futures.Future[Any]], None], Context]]) -> str: ...  # undocumented
def _future_repr_info(future: futures.Future[Any]) -> list[str]: ...  # undocumented
