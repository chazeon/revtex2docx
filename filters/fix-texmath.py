#!/usr/bin/env python3

from pandocfilters import toJSONFilter

def replaceCommands(key, value, format, meta):
    if key == "Math":
        for i in range(len(value)):
            if isinstance(value[i], str):
                value[i] = value[i].replace(r"\tiny", "")
                value[i] = value[i].replace(r"\large", "")
                value[i] = value[i].replace(r"\text", "\mathrm")

if __name__ == "__main__":
    toJSONFilter(replaceCommands)
