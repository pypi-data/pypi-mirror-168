from collections.abc import Iterable, Mapping
from typing import Any, overload
from typing_extensions import TypeAlias

_Option: TypeAlias = tuple[str, str | None, str]
_GR: TypeAlias = tuple[list[str], OptionDummy]

def fancy_getopt(
    options: list[_Option], negative_opt: Mapping[_Option, _Option], object: Any, args: list[str] | None
) -> list[str] | _GR: ...
def wrap_text(text: str, width: int) -> list[str]: ...

class FancyGetopt:
    def __init__(self, option_table: list[_Option] | None = ...) -> None: ...
    # TODO kinda wrong, `getopt(object=object())` is invalid
    @overload
    def getopt(self, args: list[str] | None = ...) -> _GR: ...
    @overload
    def getopt(self, args: list[str] | None, object: Any) -> list[str]: ...
    def get_option_order(self) -> list[tuple[str, str]]: ...
    def generate_help(self, header: str | None = ...) -> list[str]: ...

class OptionDummy:
    def __init__(self, options: Iterable[str] = ...) -> None: ...
