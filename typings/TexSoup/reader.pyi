from TexSoup.data import *
from _typeshed import Incomplete
from collections.abc import Generator

__all__ = ['read_expr', 'read_tex']

def read_tex(buf, skip_envs=(), tolerance: int = 0) -> Generator[Incomplete, None, None]: ...
def read_expr(src, skip_envs=(), tolerance: int = 0, mode=...): ...
