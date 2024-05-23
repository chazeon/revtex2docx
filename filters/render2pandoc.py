import TexSoup

def render2pandoc(citeline: str): 
    '''Render a flat tex citation line to a pandoc citation line.
    >>> render2pandoc("Sano\\ \\emph  {et~al.}")
    [{'t': 'Str', 'c': 'Sano et al.'}]
    '''
    soup = TexSoup.TexSoup(citeline)
    text = ''
    for content in soup.contents:
        if isinstance(content, TexSoup.utils.Token):
            text += "".join(content.text)

            # text += partial_text
        if isinstance(content, TexSoup.TexNode):
            text += "".join(content.text)

    text = text.replace('~', ' ')
    text = text.replace('\\ ', ' ')
        # text = text + content.text
    return [{'t': 'Str', 'c': text}]
