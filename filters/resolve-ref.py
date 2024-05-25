#!/usr/bin/env python3


import os
import sys
from pathlib import Path
from utils.render2pandoc import render2pandoc
from utils.aux import parse_refs
import panflute


def make_resolve_ref(tex_source: str):

    aux_fname = Path(tex_source).with_suffix('.aux')
    refs, bibcites = parse_refs(aux_fname)

    def resolve_ref(elem: panflute.Element, doc: panflute.Doc):

        nonlocal refs, bibcites

        if isinstance(elem, panflute.Link):
            link: panflute.Link = elem
            ref_attr = link.attributes
            # for a proper link-reference, ref_attr should look like this:
            # {'reference-type': 'ref', 'reference': 'fig:1'}
            # for a citation-reference, it would be empty
            ref_key = ref_attr.get('reference', None)
            if ref_key:
                elem.content = panflute.ListContainer(
                    panflute.Str(refs[ref_key]['ref_num'])
                )

        elif isinstance(elem, panflute.Cite):
            cite: panflute.Cite = elem
            if len(cite.citations) == 1 and cite.citations[0].mode == "AuthorInText":
                # fix AuthorInText not properly handled by citeproc
                # currently only one author-in-text citation is supported
                citation: panflute.Citation = cite.citations[0]
                if citation.mode == "AuthorInText":
                    sys.stderr.write(str(
                        cite.content
                    ) + '\n')
                    cite.content = panflute.ListContainer(
                        *render2pandoc(bibcites[citation.id]["authors_short"]),
                        panflute.Space(),
                        *cite.content
                    )

    return resolve_ref


def main(doc=None):

    tex_source = os.environ.get('PANDOC_TEX_SOURCE', None)
    if not tex_source:
        sys.stderr.write(
            "Error: PANDOC_TEX_SOURCE environment variable not set\n")
        exit(1)

    return panflute.run_filter(make_resolve_ref(tex_source), doc=doc)


if __name__ == "__main__":
    main()
