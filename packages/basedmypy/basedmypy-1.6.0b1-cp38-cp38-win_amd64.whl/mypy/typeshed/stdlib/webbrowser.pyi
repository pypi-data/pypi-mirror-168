import sys
from abc import abstractmethod
from collections.abc import Callable, Sequence
from typing_extensions import Literal

__all__ = ["Error", "open", "open_new", "open_new_tab", "get", "register"]

class Error(Exception): ...

def register(
    name: str, klass: Callable[[], BaseBrowser] | None, instance: BaseBrowser | None = ..., *, preferred: bool = ...
) -> None: ...
def get(using: str | None = ...) -> BaseBrowser: ...
def open(url: str, new: int = ..., autoraise: bool = ...) -> bool: ...
def open_new(url: str) -> bool: ...
def open_new_tab(url: str) -> bool: ...

class BaseBrowser:
    args: list[str]
    name: str
    basename: str
    def __init__(self, name: str = ...) -> None: ...
    @abstractmethod
    def open(self, url: str, new: int = ..., autoraise: bool = ...) -> bool: ...
    def open_new(self, url: str) -> bool: ...
    def open_new_tab(self, url: str) -> bool: ...

class GenericBrowser(BaseBrowser):
    def __init__(self, name: str | Sequence[str]) -> None: ...
    def open(self, url: str, new: int = ..., autoraise: bool = ...) -> bool: ...

class BackgroundBrowser(GenericBrowser): ...

class UnixBrowser(BaseBrowser):
    def open(self, url: str, new: Literal[0, 1, 2] = ..., autoraise: bool = ...) -> bool: ...  # type: ignore[override]
    raise_opts: list[str] | None
    background: bool
    redirect_stdout: bool
    remote_args: list[str]
    remote_action: str
    remote_action_newwin: str
    remote_action_newtab: str

class Mozilla(UnixBrowser): ...

class Galeon(UnixBrowser):
    raise_opts: list[str]

class Chrome(UnixBrowser): ...
class Opera(UnixBrowser): ...
class Elinks(UnixBrowser): ...

class Konqueror(BaseBrowser):
    def open(self, url: str, new: int = ..., autoraise: bool = ...) -> bool: ...

class Grail(BaseBrowser):
    def open(self, url: str, new: int = ..., autoraise: bool = ...) -> bool: ...

if sys.platform == "win32":
    class WindowsDefault(BaseBrowser):
        def open(self, url: str, new: int = ..., autoraise: bool = ...) -> bool: ...

if sys.platform == "darwin":
    class MacOSX(BaseBrowser):
        def open(self, url: str, new: int = ..., autoraise: bool = ...) -> bool: ...

    class MacOSXOSAScript(BaseBrowser):  # In runtime this class does not have `name` and `basename`
        def open(self, url: str, new: int = ..., autoraise: bool = ...) -> bool: ...
