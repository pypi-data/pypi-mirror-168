import sys
from _typeshed import SupportsRead
from collections.abc import Callable, Iterable, Iterator
from importlib.abc import Loader, MetaPathFinder, PathEntryFinder
from typing import IO, Any, NamedTuple, TypeVar

__all__ = [
    "get_importer",
    "iter_importers",
    "get_loader",
    "find_loader",
    "walk_packages",
    "iter_modules",
    "get_data",
    "ImpImporter",
    "ImpLoader",
    "read_code",
    "extend_path",
    "ModuleInfo",
]

_PathT = TypeVar("_PathT", bound=Iterable[str])

class ModuleInfo(NamedTuple):
    module_finder: MetaPathFinder | PathEntryFinder
    name: str
    ispkg: bool

def extend_path(path: _PathT, name: str) -> _PathT: ...

class ImpImporter:
    def __init__(self, path: str | None = ...) -> None: ...

class ImpLoader:
    def __init__(self, fullname: str, file: IO[str], filename: str, etc: tuple[str, str, int]) -> None: ...

def find_loader(fullname: str) -> Loader | None: ...
def get_importer(path_item: str) -> PathEntryFinder | None: ...
def get_loader(module_or_name: str) -> Loader | None: ...
def iter_importers(fullname: str = ...) -> Iterator[MetaPathFinder | PathEntryFinder]: ...
def iter_modules(path: Iterable[str] | None = ..., prefix: str = ...) -> Iterator[ModuleInfo]: ...
def read_code(stream: SupportsRead[bytes]) -> Any: ...  # undocumented
def walk_packages(
    path: Iterable[str] | None = ..., prefix: str = ..., onerror: Callable[[str], object] | None = ...
) -> Iterator[ModuleInfo]: ...
def get_data(package: str, resource: str) -> bytes | None: ...

if sys.version_info >= (3, 9):
    def resolve_name(name: str) -> Any: ...
