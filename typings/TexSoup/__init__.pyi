from TexSoup.data import TexNode as TexNode
from TexSoup.tex import read as read

__version__: str

def TexSoup(tex_code, skip_envs=(), tolerance: int = 0): ...
