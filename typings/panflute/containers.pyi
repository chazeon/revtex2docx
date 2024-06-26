from .utils import check_type as check_type, debug as debug, encode_dict as encode_dict
from _typeshed import Incomplete
from collections.abc import MutableMapping, MutableSequence

class ListContainer(MutableSequence):
    oktypes: Incomplete
    parent: Incomplete
    location: Incomplete
    list: Incomplete
    def __init__(self, *args, oktypes=..., parent: Incomplete | None = None) -> None: ...
    def __contains__(self, item) -> bool: ...
    def __len__(self) -> int: ...
    def __getitem__(self, i): ...
    def __delitem__(self, i) -> None: ...
    def __setitem__(self, i, v) -> None: ...
    def insert(self, i, v) -> None: ...
    def walk(self, action, doc: Incomplete | None = None, stop_if: Incomplete | None = None): ...
    def __eq__(self, other): ...
    def to_json(self): ...

class DictContainer(MutableMapping):
    oktypes: Incomplete
    parent: Incomplete
    location: Incomplete
    dict: Incomplete
    def __init__(self, *args, oktypes=..., parent: Incomplete | None = None, **kwargs) -> None: ...
    def __contains__(self, item) -> bool: ...
    def __len__(self) -> int: ...
    def __getitem__(self, k): ...
    def __delitem__(self, k) -> None: ...
    def __setitem__(self, k, v) -> None: ...
    def walk(self, action, doc: Incomplete | None = None, stop_if: Incomplete | None = None): ...
    def __iter__(self): ...
    def to_json(self): ...

def attach(element, parent, location, index: Incomplete | None = None): ...
def to_json_wrapper(e): ...
