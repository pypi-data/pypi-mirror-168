from collections.abc import Callable, Generator
from re import Pattern
from typing import TypeVar
from typing_extensions import TypeAlias
from xml.etree.ElementTree import Element

xpath_tokenizer_re: Pattern[str]

_Token: TypeAlias = tuple[str, str]
_Next: TypeAlias = Callable[[], _Token]
_Callback: TypeAlias = Callable[[_SelectorContext, list[Element]], Generator[Element, None, None]]

def xpath_tokenizer(pattern: str, namespaces: dict[str, str] | None = ...) -> Generator[_Token, None, None]: ...
def get_parent_map(context: _SelectorContext) -> dict[Element, Element]: ...
def prepare_child(next: _Next, token: _Token) -> _Callback: ...
def prepare_star(next: _Next, token: _Token) -> _Callback: ...
def prepare_self(next: _Next, token: _Token) -> _Callback: ...
def prepare_descendant(next: _Next, token: _Token) -> _Callback: ...
def prepare_parent(next: _Next, token: _Token) -> _Callback: ...
def prepare_predicate(next: _Next, token: _Token) -> _Callback: ...

ops: dict[str, Callable[[_Next, _Token], _Callback]]

class _SelectorContext:
    parent_map: dict[Element, Element] | None
    root: Element
    def __init__(self, root: Element) -> None: ...

_T = TypeVar("_T")

def iterfind(elem: Element, path: str, namespaces: dict[str, str] | None = ...) -> Generator[Element, None, None]: ...
def find(elem: Element, path: str, namespaces: dict[str, str] | None = ...) -> Element | None: ...
def findall(elem: Element, path: str, namespaces: dict[str, str] | None = ...) -> list[Element]: ...
def findtext(elem: Element, path: str, default: _T | None = ..., namespaces: dict[str, str] | None = ...) -> _T | str: ...
