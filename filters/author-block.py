from typing import List
import TexSoup
import os
import sys
import panflute
from utils.render2pandoc import render2pandoc


class AuthorBlock:

    def __init__(self, soup: TexSoup.data.TexNode):
        self.authors: List[dict] = []
        self._walk(soup)

    def _walk(self, soup: TexSoup.data.TexNode):
        for node in soup.contents:
            if isinstance(node, TexSoup.data.TexNode):
                if node.name == "author":
                    self.authors.append({
                        "name": node.contents,
                        "affiliations": []
                    })
                elif node.name == "affiliation":
                    self.authors[-1]["affiliations"].append(node.contents)
                else:
                    self._walk(node)

    def make_author_block(self):
        lines = []
        for author in self.authors:
            lines.append(panflute.Div(panflute.Para(
                *render2pandoc(author["name"])), attributes={
                    "class": "author",
                    "custom-style": "Author"
            }))
            for affiliation in author["affiliations"]:
                lines.append(panflute.Div(panflute.Para(*render2pandoc(affiliation)), attributes={
                    "class": "affiliation",
                    "custom-style": "Author Affiliation"
                }))
        return panflute.Div(*lines)

    def make_compressed_author_block(self):

        affiliations = {}

        for author in self.authors:
            for affiliation in author["affiliations"]:
                if str(affiliation) not in affiliations:
                    affiliations[str(affiliation)] = {
                        'id': len(affiliations) + 1,
                        'content': affiliation,
                    }

        lines = []
        author_list = []

        for author in self.authors:

            affiliation_ids = []

            for affiliation in author["affiliations"]:
                affiliation_ids.append(affiliations[str(affiliation)])

            affiliation_text = " " + ",".join(
                map(lambda x: str(x['id']), affiliation_ids))

            if len(author_list) > 0:
                author_list.append(panflute.Str(", "))

            author_list.append(panflute.Span(
                *render2pandoc(author["name"]),
                panflute.Superscript(panflute.Str(affiliation_text))
            ))

        lines.append(panflute.Div(panflute.Para(*author_list), attributes={
            "class": "author",
            "custom-style": "Author"
        }))

        for affiliation in affiliations.values():
            lines.append(panflute.Div(panflute.Para(
                panflute.Superscript(panflute.Str(
                    str(affiliation['id']) + " "
                )),
                *render2pandoc(affiliation['content'])), attributes={
                "class": "affiliation",
                "custom-style": "Author Affiliation"
            }))

        return panflute.Div(*lines)


def make_author_block(tex_source: str):

    with open(tex_source) as f:
        soup = TexSoup.TexSoup(f.read())

    author_block = AuthorBlock(soup)

    def add_author_block(doc: panflute.Doc):
        # if isinstance(elem, panflute.MetaMap):
        # elem["author-block"] = author_block.make_author_block()
        # elem["compressed-author-block"] = author_block.make_compressed_author_block()
        # sys.stderr.write(str(doc.metadata["author"]))
        doc.metadata["author"].clear()
        doc.content.insert(0, author_block.make_compressed_author_block())

    return add_author_block


def main(doc=None):

    tex_source = os.environ.get('PANDOC_TEX_SOURCE', None)
    if not tex_source:
        sys.stderr.write(
            "Error: PANDOC_TEX_SOURCE environment variable not set\n")
        exit(1)

    return panflute.run_filters([], prepare=make_author_block(tex_source=tex_source), doc=doc)


if __name__ == "__main__":
    # make_author_block(sys.argv[1])
    main()
