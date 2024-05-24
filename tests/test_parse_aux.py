from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent / "filters"))

import utils.aux as aux

def test_parse_aux():
    test_dir = Path(__file__).parent
    aux.parse_refs(str(test_dir / 'lorem/lorem.aux'))
