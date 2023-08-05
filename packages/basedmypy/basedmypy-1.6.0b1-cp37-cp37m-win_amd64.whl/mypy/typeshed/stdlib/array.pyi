import sys
from _typeshed import ReadableBuffer, Self, SupportsRead, SupportsWrite
from collections.abc import Iterable

# pytype crashes if array inherits from collections.abc.MutableSequence instead of typing.MutableSequence
from typing import Any, Generic, MutableSequence, TypeVar, overload  # noqa: Y027
from typing_extensions import Literal, SupportsIndex, TypeAlias

_IntTypeCode: TypeAlias = Literal["b", "B", "h", "H", "i", "I", "l", "L", "q", "Q"]
_FloatTypeCode: TypeAlias = Literal["f", "d"]
_UnicodeTypeCode: TypeAlias = Literal["u"]
_TypeCode: TypeAlias = _IntTypeCode | _FloatTypeCode | _UnicodeTypeCode

_T = TypeVar("_T", int, float, str)

typecodes: str

class array(MutableSequence[_T], Generic[_T]):
    @property
    def typecode(self) -> _TypeCode: ...
    @property
    def itemsize(self) -> int: ...
    @overload
    def __init__(self: array[int], __typecode: _IntTypeCode, __initializer: bytes | Iterable[int] = ...) -> None: ...
    @overload
    def __init__(self: array[float], __typecode: _FloatTypeCode, __initializer: bytes | Iterable[float] = ...) -> None: ...
    @overload
    def __init__(self: array[str], __typecode: _UnicodeTypeCode, __initializer: bytes | Iterable[str] = ...) -> None: ...
    @overload
    def __init__(self, __typecode: str, __initializer: Iterable[_T]) -> None: ...
    @overload
    def __init__(self, __typecode: str, __initializer: bytes = ...) -> None: ...
    def append(self, __v: _T) -> None: ...
    def buffer_info(self) -> tuple[int, int]: ...
    def byteswap(self) -> None: ...
    def count(self, __v: _T) -> int: ...
    def extend(self, __bb: Iterable[_T]) -> None: ...
    def frombytes(self, __buffer: ReadableBuffer) -> None: ...
    def fromfile(self, __f: SupportsRead[bytes], __n: int) -> None: ...
    def fromlist(self, __list: list[_T]) -> None: ...
    def fromunicode(self, __ustr: str) -> None: ...
    if sys.version_info >= (3, 10):
        def index(self, __v: _T, __start: int = ..., __stop: int = ...) -> int: ...
    else:
        def index(self, __v: _T) -> int: ...  # type: ignore[override]

    def insert(self, __i: int, __v: _T) -> None: ...
    def pop(self, __i: int = ...) -> _T: ...
    def remove(self, __v: _T) -> None: ...
    def tobytes(self) -> bytes: ...
    def tofile(self, __f: SupportsWrite[bytes]) -> None: ...
    def tolist(self) -> list[_T]: ...
    def tounicode(self) -> str: ...
    if sys.version_info < (3, 9):
        def fromstring(self, __buffer: bytes) -> None: ...
        def tostring(self) -> bytes: ...

    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, __i: SupportsIndex) -> _T: ...
    @overload
    def __getitem__(self, __s: slice) -> array[_T]: ...
    @overload  # type: ignore[override]
    def __setitem__(self, __i: SupportsIndex, __o: _T) -> None: ...
    @overload
    def __setitem__(self, __s: slice, __o: array[_T]) -> None: ...
    def __delitem__(self, __i: SupportsIndex | slice) -> None: ...
    def __add__(self, __x: array[_T]) -> array[_T]: ...
    def __ge__(self, __other: array[_T]) -> bool: ...
    def __gt__(self, __other: array[_T]) -> bool: ...
    def __iadd__(self: Self, __x: array[_T]) -> Self: ...  # type: ignore[override]
    def __imul__(self: Self, __n: int) -> Self: ...
    def __le__(self, __other: array[_T]) -> bool: ...
    def __lt__(self, __other: array[_T]) -> bool: ...
    def __mul__(self, __n: int) -> array[_T]: ...
    def __rmul__(self, __n: int) -> array[_T]: ...
    def __copy__(self) -> array[_T]: ...
    def __deepcopy__(self, __unused: Any) -> array[_T]: ...

ArrayType = array
