
import filters.aux as aux
from pathlib import Path


def test_parse_aux():
    test_dir = Path(__file__).parent
    aux.parse_refs(str(test_dir / 'lorem/lorem.aux'))
