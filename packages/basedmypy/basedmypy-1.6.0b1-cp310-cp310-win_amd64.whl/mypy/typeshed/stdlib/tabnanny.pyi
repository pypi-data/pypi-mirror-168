from _typeshed import StrOrBytesPath
from collections.abc import Iterable

__all__ = ["check", "NannyNag", "process_tokens"]

verbose: int
filename_only: int

class NannyNag(Exception):
    def __init__(self, lineno: int, msg: str, line: str) -> None: ...
    def get_lineno(self) -> int: ...
    def get_msg(self) -> str: ...
    def get_line(self) -> str: ...

def check(file: StrOrBytesPath) -> None: ...
def process_tokens(tokens: Iterable[tuple[int, str, tuple[int, int], tuple[int, int], str]]) -> None: ...
