import sys
from _typeshed import (
    OpenBinaryMode,
    OpenBinaryModeReading,
    OpenBinaryModeUpdating,
    OpenBinaryModeWriting,
    OpenTextMode,
    Self,
    StrPath,
)
from collections.abc import Generator, Sequence
from io import BufferedRandom, BufferedReader, BufferedWriter, FileIO, TextIOWrapper
from os import PathLike, stat_result
from types import TracebackType
from typing import IO, Any, BinaryIO, overload
from typing_extensions import Literal

if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = ["PurePath", "PurePosixPath", "PureWindowsPath", "Path", "PosixPath", "WindowsPath"]

class PurePath(PathLike[str]):
    @property
    def parts(self) -> tuple[str, ...]: ...
    @property
    def drive(self) -> str: ...
    @property
    def root(self) -> str: ...
    @property
    def anchor(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def suffix(self) -> str: ...
    @property
    def suffixes(self) -> list[str]: ...
    @property
    def stem(self) -> str: ...
    def __new__(cls: type[Self], *args: StrPath) -> Self: ...
    def __eq__(self, other: object) -> bool: ...
    def __fspath__(self) -> str: ...
    def __lt__(self, other: PurePath) -> bool: ...
    def __le__(self, other: PurePath) -> bool: ...
    def __gt__(self, other: PurePath) -> bool: ...
    def __ge__(self, other: PurePath) -> bool: ...
    def __truediv__(self: Self, key: StrPath) -> Self: ...
    def __rtruediv__(self: Self, key: StrPath) -> Self: ...
    def __bytes__(self) -> bytes: ...
    def as_posix(self) -> str: ...
    def as_uri(self) -> str: ...
    def is_absolute(self) -> bool: ...
    def is_reserved(self) -> bool: ...
    if sys.version_info >= (3, 9):
        def is_relative_to(self, *other: StrPath) -> bool: ...

    def match(self, path_pattern: str) -> bool: ...
    def relative_to(self: Self, *other: StrPath) -> Self: ...
    def with_name(self: Self, name: str) -> Self: ...
    if sys.version_info >= (3, 9):
        def with_stem(self: Self, stem: str) -> Self: ...

    def with_suffix(self: Self, suffix: str) -> Self: ...
    def joinpath(self: Self, *other: StrPath) -> Self: ...
    @property
    def parents(self: Self) -> Sequence[Self]: ...
    @property
    def parent(self: Self) -> Self: ...
    if sys.version_info >= (3, 9) and sys.version_info < (3, 11):
        def __class_getitem__(cls, type: Any) -> GenericAlias: ...

class PurePosixPath(PurePath): ...
class PureWindowsPath(PurePath): ...

class Path(PurePath):
    def __new__(cls: type[Self], *args: StrPath, **kwargs: Any) -> Self: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, t: type[BaseException] | None, v: BaseException | None, tb: TracebackType | None) -> None: ...
    @classmethod
    def cwd(cls: type[Self]) -> Self: ...
    if sys.version_info >= (3, 10):
        def stat(self, *, follow_symlinks: bool = ...) -> stat_result: ...
        def chmod(self, mode: int, *, follow_symlinks: bool = ...) -> None: ...
    else:
        def stat(self) -> stat_result: ...
        def chmod(self, mode: int) -> None: ...

    def exists(self) -> bool: ...
    def glob(self: Self, pattern: str) -> Generator[Self, None, None]: ...
    def is_dir(self) -> bool: ...
    def is_file(self) -> bool: ...
    def is_symlink(self) -> bool: ...
    def is_socket(self) -> bool: ...
    def is_fifo(self) -> bool: ...
    def is_block_device(self) -> bool: ...
    def is_char_device(self) -> bool: ...
    def iterdir(self: Self) -> Generator[Self, None, None]: ...
    def lchmod(self, mode: int) -> None: ...
    def lstat(self) -> stat_result: ...
    def mkdir(self, mode: int = ..., parents: bool = ..., exist_ok: bool = ...) -> None: ...
    # Adapted from builtins.open
    # Text mode: always returns a TextIOWrapper
    # The Traversable .open in stdlib/importlib/abc.pyi should be kept in sync with this.
    @overload
    def open(
        self,
        mode: OpenTextMode = ...,
        buffering: int = ...,
        encoding: str | None = ...,
        errors: str | None = ...,
        newline: str | None = ...,
    ) -> TextIOWrapper: ...
    # Unbuffered binary mode: returns a FileIO
    @overload
    def open(
        self, mode: OpenBinaryMode, buffering: Literal[0], encoding: None = ..., errors: None = ..., newline: None = ...
    ) -> FileIO: ...
    # Buffering is on: return BufferedRandom, BufferedReader, or BufferedWriter
    @overload
    def open(
        self,
        mode: OpenBinaryModeUpdating,
        buffering: Literal[-1, 1] = ...,
        encoding: None = ...,
        errors: None = ...,
        newline: None = ...,
    ) -> BufferedRandom: ...
    @overload
    def open(
        self,
        mode: OpenBinaryModeWriting,
        buffering: Literal[-1, 1] = ...,
        encoding: None = ...,
        errors: None = ...,
        newline: None = ...,
    ) -> BufferedWriter: ...
    @overload
    def open(
        self,
        mode: OpenBinaryModeReading,
        buffering: Literal[-1, 1] = ...,
        encoding: None = ...,
        errors: None = ...,
        newline: None = ...,
    ) -> BufferedReader: ...
    # Buffering cannot be determined: fall back to BinaryIO
    @overload
    def open(
        self, mode: OpenBinaryMode, buffering: int = ..., encoding: None = ..., errors: None = ..., newline: None = ...
    ) -> BinaryIO: ...
    # Fallback if mode is not specified
    @overload
    def open(
        self, mode: str, buffering: int = ..., encoding: str | None = ..., errors: str | None = ..., newline: str | None = ...
    ) -> IO[Any]: ...
    if sys.platform != "win32":
        # These methods do "exist" on Windows, but they always raise NotImplementedError,
        # so it's safer to pretend they don't exist
        def owner(self) -> str: ...
        def group(self) -> str: ...
        def is_mount(self) -> bool: ...

    if sys.version_info >= (3, 9):
        def readlink(self: Self) -> Self: ...
    if sys.version_info >= (3, 8):
        def rename(self: Self, target: str | PurePath) -> Self: ...
        def replace(self: Self, target: str | PurePath) -> Self: ...
    else:
        def rename(self, target: str | PurePath) -> None: ...
        def replace(self, target: str | PurePath) -> None: ...

    def resolve(self: Self, strict: bool = ...) -> Self: ...
    def rglob(self: Self, pattern: str) -> Generator[Self, None, None]: ...
    def rmdir(self) -> None: ...
    def symlink_to(self, target: str | Path, target_is_directory: bool = ...) -> None: ...
    if sys.version_info >= (3, 10):
        def hardlink_to(self, target: str | Path) -> None: ...

    def touch(self, mode: int = ..., exist_ok: bool = ...) -> None: ...
    if sys.version_info >= (3, 8):
        def unlink(self, missing_ok: bool = ...) -> None: ...
    else:
        def unlink(self) -> None: ...

    @classmethod
    def home(cls: type[Self]) -> Self: ...
    def absolute(self: Self) -> Self: ...
    def expanduser(self: Self) -> Self: ...
    def read_bytes(self) -> bytes: ...
    def read_text(self, encoding: str | None = ..., errors: str | None = ...) -> str: ...
    def samefile(self, other_path: str | bytes | int | Path) -> bool: ...
    def write_bytes(self, data: bytes) -> int: ...
    if sys.version_info >= (3, 10):
        def write_text(
            self, data: str, encoding: str | None = ..., errors: str | None = ..., newline: str | None = ...
        ) -> int: ...
    else:
        def write_text(self, data: str, encoding: str | None = ..., errors: str | None = ...) -> int: ...
    if sys.version_info >= (3, 8):
        def link_to(self, target: StrPath | bytes) -> None: ...

class PosixPath(Path, PurePosixPath): ...
class WindowsPath(Path, PureWindowsPath): ...
