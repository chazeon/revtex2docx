import TexSoup
from typing import Tuple, Dict, Union


def read_aux(fname: str) -> TexSoup.data.TexNode:
    with open(fname) as f:
        return TexSoup.TexSoup(f.read())


def parse_refs(fname: str) -> Tuple[Dict, Dict]:

    soup = read_aux(fname)
    refs = {}  # type: Dict[str, Dict[str, str]]
    # type: Dict[str, Dict[str, Union[str, TexSoup.data.BraceGroup]]]
    bibcites = {}

    for node in soup.contents:
        if isinstance(node, TexSoup.data.TexNode):
            # handle \newlabel command
            if node.name == "newlabel":
                ref_label = node.args[0].contents[0]  # type: str
                if len(node.args[1].contents[0].contents) > 0:
                    ref_number = node.args[1].contents[0].contents[0]
                else:
                    ref_number = ""
                refs[ref_label] = {
                    "label": ref_label,
                    "ref_num": ref_number
                }
            elif node.name == "bibcite":
                # handle \bibcite command

                cite_key = node.args[0].contents[0]  # type: str
                cite_info = node.args[1]

                cite_ref_number = cite_info.contents[0].contents[0]
                cite_year = cite_info.contents[1].contents[0]
                cite_authors_short = cite_info.contents[2].contents[0]
                cite_authors_full = cite_info.contents[3].contents[0]

                bibcites[cite_key] = {
                    "key": cite_key,
                    "ref_num": cite_ref_number,
                    "year": cite_year,
                    "authors_short": str(cite_authors_short),
                    "authors_full": str(cite_authors_full),
                }

    return refs, bibcites


if __name__ == "__main__":
    import sys
    from pprint import pprint
    pprint(parse_refs(sys.argv[1]))
