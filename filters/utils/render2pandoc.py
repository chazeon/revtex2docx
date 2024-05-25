import TexSoup
from panflute import Str, Space, ListContainer, Emph


def render2pandoc(citeline: str) -> ListContainer:
    r'''Render a flat tex citation line to a pandoc citation line.
    >>> render2pandoc("Sano\\ \\emph  {et~al.}").to_json()
    [{'t': 'Str', 'c': 'Sano'}, {'t': 'Space'}, {'t': 'Emph', 'c': [{'t': 'Str', 'c': 'et al.'}]}]
    >>> render2pandoc("{Sano\\ \\emph  {et~al.}}").to_json()
    [{'t': 'Str', 'c': 'Sano'}, {'t': 'Space'}, {'t': 'Emph', 'c': [{'t': 'Str', 'c': 'et al.'}]}]
    '''

    soup = TexSoup.TexSoup(citeline)

    def walk(soup: TexSoup.data.TexNode):
        for content in soup.contents:
            if isinstance(content, TexSoup.data.TexNode):
                if content.name == 'emph':
                    yield Emph(*walk(content))
                else:
                    for item in walk(content):
                        yield item
            elif isinstance(content, TexSoup.utils.Token):
                if str(content) == r"\ ":
                    yield Space()
                else:
                    text = str(content)
                    text = text.replace('~', ' ')
                    yield Str(text)
            else:
                yield content

    return ListContainer(*walk(soup))
