import sys
from _typeshed import structseq
from typing import Any
from typing_extensions import Final, final

if sys.platform != "win32":
    @final
    class struct_group(structseq[Any], tuple[str, str | None, int, list[str]]):
        if sys.version_info >= (3, 10):
            __match_args__: Final = ("gr_name", "gr_passwd", "gr_gid", "gr_mem")
        @property
        def gr_name(self) -> str: ...
        @property
        def gr_passwd(self) -> str | None: ...
        @property
        def gr_gid(self) -> int: ...
        @property
        def gr_mem(self) -> list[str]: ...

    def getgrall() -> list[struct_group]: ...
    def getgrgid(id: int) -> struct_group: ...
    def getgrnam(name: str) -> struct_group: ...
