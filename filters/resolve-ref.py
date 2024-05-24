#!/usr/bin/env python3


import re
from pandocfilters import toJSONFilter
from functools import lru_cache
from utils.render2pandoc import render2pandoc

REF_REGEX = re.compile(r'^\\newlabel{(.+)}{{(.+)}{(.*)}{(.*)}{(.*)}{(.*)}}$')
BIBCITE_REGEX = re.compile(r'^\\bibcite\{(.*)\}\{\{(.*)\}\{(.*)\}\{\{(.*)\}\}\{\{(.*)\}\}\}$')

@lru_cache
def load_aux(fname: str) -> tuple[dict, dict]:
    refs = {}
    bibcites = {}
    with open(fname) as fp:
        for line in fp:
            res = REF_REGEX.search(line)

            if res:
                refs[res.group(1)] = res.group(2)

            res = BIBCITE_REGEX.search(line)
            if res:
                bibcites[res.group(1)] = {
                    "ref_num": res.group(2),
                    "year": res.group(3), 
                    "authors_short": res.group(4),
                    "authors_full": res.group(5),
                }
            
    return refs, bibcites

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
        except Exception as e:
            pass
    
    elif key == "Cite":
        # fix AuthorInText not properly handled by citeproc
        cite_info = value[0][0]
        try:
            if cite_info["citationMode"]['t'] == "AuthorInText":
                value[1] = [
                    *render2pandoc(bibcites[cite_info["citationId"]]["authors_short"]),
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