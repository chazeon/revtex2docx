from .io import dump as dump, load as load
from .utils import ContextImport as ContextImport, debug as debug
from _typeshed import Incomplete

reduced_sys_path: Incomplete

def get_filter_dirs(hardcoded: bool = True): ...
def stdio(filters: Incomplete | None = None, search_dirs: Incomplete | None = None, data_dir: bool = True, sys_path: bool = True, panfl_: bool = False, input_stream: Incomplete | None = None, output_stream: Incomplete | None = None) -> None: ...
def main() -> None: ...

help_str: str

def panfl(filters, to, search_dirs, data_dir, sys_path) -> None: ...
def autorun_filters(filters, doc, search_dirs, verbose): ...
