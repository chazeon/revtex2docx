import TexSoup
import panflute
import os
import sys
from typing import List


class EquationRegistry:

    def __init__(self, soup: TexSoup.data.TexNode):
        self.data: List[TexSoup.data.TexNode] = []
        self._walk(soup)

    def _walk(self, soup: TexSoup.data.TexNode):
        for node in soup.contents:
            if isinstance(node, TexSoup.data.TexNode):
                if node.name == "document":
                    self._walk(node)
                if node.name in {"displaymath", "equation", "equation*", "subequations"}:
                    self.data.append(node)


def make_add_eqn_no(tex_source: str):

    with open(tex_source) as f:
        soup = TexSoup.TexSoup(f.read())

    registry = EquationRegistry(soup)

    count = 0
    eqn_no = 1

    def add_eqn_no(elem, doc):
        nonlocal count, eqn_no
        if isinstance(elem, panflute.Math) and elem.format == "DisplayMath":
            if registry.data[count].name in {"equation", "equation*", "align"}:
                lines = elem.text.splitlines()
                lines.append(rf"\qquad ({eqn_no})")
                elem.text = "\n".join(lines)
                eqn_no += 1
            count += 1

    return add_eqn_no


def main(doc=None):

    tex_source = os.environ.get('PANDOC_TEX_SOURCE', None)
    if not tex_source:
        sys.stderr.write(
            "Error: PANDOC_TEX_SOURCE environment variable not set\n")
        exit(1)

    return panflute.run_filter(make_add_eqn_no(tex_source), doc=doc)


if __name__ == "__main__":
    main()
