from _typeshed import WriteableBuffer
from collections.abc import Callable
from io import DEFAULT_BUFFER_SIZE, BufferedIOBase, RawIOBase
from typing import Any, Protocol

BUFFER_SIZE = DEFAULT_BUFFER_SIZE

class _Reader(Protocol):
    def read(self, __n: int) -> bytes: ...
    def seekable(self) -> bool: ...
    def seek(self, __n: int) -> Any: ...

class BaseStream(BufferedIOBase): ...

class DecompressReader(RawIOBase):
    def __init__(
        self,
        fp: _Reader,
        decomp_factory: Callable[..., object],
        trailing_error: type[Exception] | tuple[type[Exception], ...] = ...,
        **decomp_args: Any,
    ) -> None: ...
    def readinto(self, b: WriteableBuffer) -> int: ...
    def read(self, size: int = ...) -> bytes: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...
