import TexSoup


def render2pandoc(citeline: str):
    r'''Render a flat tex citation line to a pandoc citation line.
    >>> render2pandoc("Sano\\ \\emph  {et~al.}")
    [{'t': 'Str', 'c': 'Sano'}, {'t': 'Str', 'c': '\\ '}, {'t': 'Emph', 'c': [{'t': 'Str', 'c': 'et~al.'}]}]
    '''

    soup = TexSoup.TexSoup(citeline)

    def walk(soup: TexSoup.data.TexNode):
        for content in soup.contents:
            if isinstance(content, TexSoup.data.TexNode):
                if content.name == 'emph':
                    yield {
                        't': 'Emph',
                        'c': list(walk(content))
                    }
                else:
                    yield walk(content)
            elif isinstance(content, TexSoup.utils.Token):
                if str(content) == r"\\ ":
                    yield {'t': 'Space'}
                else:
                    text = str(content)
                    text.replace('~', ' ')
                    yield {'t': 'Str', 'c': text}
            else:
                yield content

    return list(walk(soup))
