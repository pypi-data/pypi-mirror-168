import sys
from _typeshed import Self
from collections.abc import Iterable
from typing import Any, Generic, TypeVar, overload

if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = ["SharedMemory", "ShareableList"]

_SLT = TypeVar("_SLT", int, float, bool, str, bytes, None)

class SharedMemory:
    def __init__(self, name: str | None = ..., create: bool = ..., size: int = ...) -> None: ...
    @property
    def buf(self) -> memoryview: ...
    @property
    def name(self) -> str: ...
    @property
    def size(self) -> int: ...
    def close(self) -> None: ...
    def unlink(self) -> None: ...

class ShareableList(Generic[_SLT]):
    shm: SharedMemory
    @overload
    def __init__(self, sequence: None = ..., *, name: str | None = ...) -> None: ...
    @overload
    def __init__(self, sequence: Iterable[_SLT], *, name: str | None = ...) -> None: ...
    def __getitem__(self, position: int) -> _SLT: ...
    def __setitem__(self, position: int, value: _SLT) -> None: ...
    def __reduce__(self: Self) -> tuple[Self, tuple[_SLT, ...]]: ...
    def __len__(self) -> int: ...
    @property
    def format(self) -> str: ...
    def count(self, value: _SLT) -> int: ...
    def index(self, value: _SLT) -> int: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...
