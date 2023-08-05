from _typeshed import OptExcInfo, StrOrBytesPath
from collections.abc import Callable
from types import FrameType, TracebackType
from typing import IO, Any

__UNDEF__: object  # undocumented sentinel

def reset() -> str: ...  # undocumented
def small(text: str) -> str: ...  # undocumented
def strong(text: str) -> str: ...  # undocumented
def grey(text: str) -> str: ...  # undocumented
def lookup(name: str, frame: FrameType, locals: dict[str, Any]) -> tuple[str | None, Any]: ...  # undocumented
def scanvars(
    reader: Callable[[], bytes], frame: FrameType, locals: dict[str, Any]
) -> list[tuple[str, str | None, Any]]: ...  # undocumented
def html(einfo: OptExcInfo, context: int = ...) -> str: ...
def text(einfo: OptExcInfo, context: int = ...) -> str: ...

class Hook:  # undocumented
    def __init__(
        self,
        display: int = ...,
        logdir: StrOrBytesPath | None = ...,
        context: int = ...,
        file: IO[str] | None = ...,
        format: str = ...,
    ) -> None: ...
    def __call__(self, etype: type[BaseException] | None, evalue: BaseException | None, etb: TracebackType | None) -> None: ...
    def handle(self, info: OptExcInfo | None = ...) -> None: ...

def handler(info: OptExcInfo | None = ...) -> None: ...
def enable(display: int = ..., logdir: StrOrBytesPath | None = ..., context: int = ..., format: str = ...) -> None: ...
