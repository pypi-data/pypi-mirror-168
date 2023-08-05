from typing import BinaryIO

__all__ = ["encode", "decode", "encodestring", "decodestring"]

def encode(input: BinaryIO, output: BinaryIO, quotetabs: int, header: int = ...) -> None: ...
def encodestring(s: bytes, quotetabs: int = ..., header: int = ...) -> bytes: ...
def decode(input: BinaryIO, output: BinaryIO, header: int = ...) -> None: ...
def decodestring(s: bytes, header: int = ...) -> bytes: ...
