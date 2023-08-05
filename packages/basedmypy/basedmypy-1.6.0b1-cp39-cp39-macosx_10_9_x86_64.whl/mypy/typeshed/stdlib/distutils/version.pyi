from _typeshed import Self
from abc import abstractmethod
from re import Pattern

class Version:
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self: Self, other: Self | str) -> bool: ...
    def __le__(self: Self, other: Self | str) -> bool: ...
    def __gt__(self: Self, other: Self | str) -> bool: ...
    def __ge__(self: Self, other: Self | str) -> bool: ...
    @abstractmethod
    def __init__(self, vstring: str | None = ...) -> None: ...
    @abstractmethod
    def parse(self: Self, vstring: str) -> Self: ...
    @abstractmethod
    def __str__(self) -> str: ...
    @abstractmethod
    def _cmp(self: Self, other: Self | str) -> bool: ...

class StrictVersion(Version):
    version_re: Pattern[str]
    version: tuple[int, int, int]
    prerelease: tuple[str, int] | None
    def __init__(self, vstring: str | None = ...) -> None: ...
    def parse(self: Self, vstring: str) -> Self: ...
    def __str__(self) -> str: ...  # noqa: Y029
    def _cmp(self: Self, other: Self | str) -> bool: ...

class LooseVersion(Version):
    component_re: Pattern[str]
    vstring: str
    version: tuple[str | int, ...]
    def __init__(self, vstring: str | None = ...) -> None: ...
    def parse(self: Self, vstring: str) -> Self: ...
    def __str__(self) -> str: ...  # noqa: Y029
    def _cmp(self: Self, other: Self | str) -> bool: ...
