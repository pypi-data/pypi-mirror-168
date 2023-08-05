import sys
import types
from _typeshed import ReadableBuffer
from importlib.machinery import ModuleSpec
from typing import Any

check_hash_based_pycs: str

def source_hash(key: int, source: ReadableBuffer) -> bytes: ...
def create_builtin(__spec: ModuleSpec) -> types.ModuleType: ...
def create_dynamic(__spec: ModuleSpec, __file: Any = ...) -> types.ModuleType: ...
def acquire_lock() -> None: ...
def exec_builtin(__mod: types.ModuleType) -> int: ...
def exec_dynamic(__mod: types.ModuleType) -> int: ...
def extension_suffixes() -> list[str]: ...
def init_frozen(__name: str) -> types.ModuleType: ...
def is_builtin(__name: str) -> int: ...
def is_frozen(__name: str) -> bool: ...
def is_frozen_package(__name: str) -> bool: ...
def lock_held() -> bool: ...
def release_lock() -> None: ...

if sys.version_info >= (3, 11):
    def find_frozen(__name: str, *, withdata: bool = ...) -> tuple[memoryview | None, bool, str | None] | None: ...
    def get_frozen_object(__name: str, __data: ReadableBuffer | None = ...) -> types.CodeType: ...

else:
    def get_frozen_object(__name: str) -> types.CodeType: ...
