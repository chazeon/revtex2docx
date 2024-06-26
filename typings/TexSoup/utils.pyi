from _typeshed import Incomplete

def IntEnum(name, keys, start: int = 1): ...

CC: Incomplete
TC: Incomplete

class Token(str):
    text: Incomplete
    position: Incomplete
    category: Incomplete
    def __new__(cls, text: str = '', position: Incomplete | None = None, category: Incomplete | None = None): ...
    def __getattr__(self, name): ...
    def __eq__(self, other): ...
    def __hash__(self): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...
    def __iadd__(self, other): ...
    @classmethod
    def join(cls, tokens, glue: str = ''): ...
    def __bool__(self) -> bool: ...
    def __contains__(self, item) -> bool: ...
    def __iter__(self): ...
    def __getitem__(self, i): ...
    def strip(self, *args, **kwargs): ...
    def lstrip(self, *args, **kwargs): ...
    def rstrip(self, *args, **kwargs): ...

class Buffer:
    def __init__(self, iterator, join=..., empty=..., init=...) -> None: ...
    def hasNext(self, n: int = 1): ...
    def startswith(self, s): ...
    def endswith(self, s): ...
    def forward(self, j: int = 1): ...
    def num_forward_until(self, condition): ...
    def forward_until(self, condition, peek: bool = True): ...
    def backward(self, j: int = 1): ...
    def peek(self, j: int = 0): ...
    def __next__(self): ...
    def __getitem__(self, i): ...
    def __iter__(self): ...
    @property
    def position(self): ...

class CharToLineOffset:
    line_break_positions: Incomplete
    src_len: Incomplete
    def __init__(self, src) -> None: ...
    def __call__(self, char_pos): ...

class MixedBuffer(Buffer):
    def __init__(self, iterator) -> None: ...

def to_buffer(convert_in: bool = True, convert_out: bool = True, Buffer=...): ...
def to_list(f): ...
