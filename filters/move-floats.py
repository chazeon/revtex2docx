import sys
import re

def extract_floats(text, patterns):
    floats = []

    for pattern in patterns:
        floats += re.findall(pattern, text, re.DOTALL)

    return floats

def main():
    content = sys.stdin.read()

    # Extract floats and remove them from the original content
    float_patterns = [
        r'\\begin\{table\}.*?\\end\{table\}',
        r'\\begin\{figure\}.*?\\end\{figure\}',
    ]
    
    floats = extract_floats(content, float_patterns)
    
    for float_content in floats:
        content = content.replace(float_content, '', 1)

    # Insert floats before '\end{document}'
    end_document_position = content.rfind('\\end{document}')
    if end_document_position != -1:
        content = content[:end_document_position] + '\n\clearpage\n'.join(floats) + '\n' + content[end_document_position:]
    else:
        content += '\n'.join(floats)

    sys.stdout.write(content)

if __name__ == '__main__':
    main()