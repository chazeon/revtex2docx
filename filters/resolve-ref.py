#!/usr/bin/env python3


import re
from pandocfilters import toJSONFilter
from functools import lru_cache
from utils.render2pandoc import render2pandoc
from utils.aux import parse_refs


@lru_cache
def load_aux(fname: str) -> tuple[dict, dict]:
    return parse_refs(fname)


fdebug = open('debug.txt', 'w')


def resolveRef(key, value, format, meta):

    refs, bibcites = load_aux('tests/lorem/lorem.aux')
    # fdebug.write(str(bibcites) + '\n')

    if key == "Link":
        ref_info = dict(value[0][2])
        # for a proper link-reference, the value[0][2] should look like this:
        # {'reference-type': 'ref', 'reference': 'fig:1'}
        # for a citation-reference, it would be empty
        try:
            ref_key = ref_info['reference']
            value[1][0]['c'] = refs[ref_key].replace(r'\,', ' ')
        except Exception:
            pass

    elif key == "Cite":
        # fix AuthorInText not properly handled by citeproc
        cite_info = value[0][0]
        try:
            if cite_info["citationMode"]['t'] == "AuthorInText":
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
            fdebug.write(str(e) + '\n')
        fdebug.write(str(value) + '\n')


if __name__ == "__main__":
    toJSONFilter(resolveRef)

fdebug.close()
