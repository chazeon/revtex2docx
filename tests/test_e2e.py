import subprocess
import pathlib

def test_e2e(tmpdir):
    test_dir = pathlib.Path(__file__).parent
    process = subprocess.Popen(
        [
            'pandoc',
            f'{test_dir}/lorem/lorem.tex',
            '--bibliography', f'{test_dir}/lorem/lorem.bib',
            '--citeproc',
            '-M', 'reference-section-title=References',
            '--filter', 'filters/resolve-ref.py',
            '-t', 'plain',
            '--eol', 'lf',
            '-o', f'{tmpdir}/output.txt'
        ],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    out, _ = process.communicate()

    assert process.returncode == 0

    with open(f'{tmpdir}/output.txt') as f:
        text = f.read()
        # print(text)
        blocks = []
        for block in text.split('\n\n'):
            block_text = " ".join(block.splitlines())
            blocks.append(block_text)
        text = "\n\n".join(blocks)
        print(text)
        assert " ".join([
            "The text is organized as follows: Section II describes the methods.",
            "Section III presents the results. Section IV discusses the results.",
            "Section V concludes the paper."
        ]) in text

