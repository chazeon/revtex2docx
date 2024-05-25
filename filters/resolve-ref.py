#!/usr/bin/env python3


import os
import sys
from pathlib import Path
from pandocfilters import toJSONFilter
from functools import lru_cache
from utils.render2pandoc import render2pandoc
from utils.aux import parse_refs


@lru_cache
def load_aux(fname: str) -> tuple[dict, dict]:
    return parse_refs(fname)


def resolveRef(key, value, format, meta):

    tex_source = os.environ.get('PANDOC_TEX_SOURCE', None)
    if not tex_source:
        sys.stderr.write("Error: PANDOC_TEX_SOURCE environment variable not set\n")
        exit(1)

    aux_fname = Path(tex_source).with_suffix('.aux')

    refs, bibcites = load_aux(aux_fname)
    # fdebug.write(str(bibcites) + '\n')

    if key == "Link":
        ref_info = dict(value[0][2])
        # for a proper link-reference, the value[0][2] should look like this:
        # {'reference-type': 'ref', 'reference': 'fig:1'}
        # for a citation-reference, it would be empty
        ref_key = ref_info.get('reference', None)
        if ref_key:
            value[1][0]['c'] = refs[ref_key]['ref_num']

    elif key == "Cite":
        # fix AuthorInText not properly handled by citeproc
        cite_info = value[0][0]
        try:
            if cite_info["citationMode"]['t'] == "AuthorInText":

                sys.stderr.write(str(
                    render2pandoc(bibcites[cite_info["citationId"]]["authors_short"])
                ) + '\n')
                value[1] = [
                    *render2pandoc(bibcites[cite_info["citationId"]]["authors_short"])[0],
                    {'t': 'Space'},
                    *value[1]
                ]
                # value[1].insert(0, {
                #     't': 'Space'
                # })
                # value[1].insert(0, )
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
        sys.stderr.write(str(value) + '\n')


if __name__ == "__main__":
    toJSONFilter(resolveRef)

fdebug.close()
