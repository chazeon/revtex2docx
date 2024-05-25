import subprocess
import pathlib
import sys


def main():

    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} [options] <tex-file>')
        print('Generate a plain text file from a LaTeX file with references resolved.')
        print('The arguments are passed to pandoc. The --citeproc option is always enabled.')
        print('Some options include:')
        print('  --bibliography <bib-file>: Specify bibliography file')
        print('  --csl <csl-file>: Specify CSL file')
        print('  -t, --to <format>: Specify output format')
        print('  --output <output-file>: Specify output file')
        print('  --reference-doc <doc-file>: Specify reference document')
        exit(255)

    fntex = next(
        (arg for arg in sys.argv[1:] if not arg.startswith('-')), None)

    if fntex is None:
        print('No tex file specified')
        exit(255)

    fntex = pathlib.Path(fntex)
    if fntex.suffix != '.tex':
        print('Invalid file type')
        exit(255)

    fnaux = fntex.with_suffix('.aux')
    if not fnaux.exists():
        print('Auxiliary file {fnaux} not found')
        exit(255)

    process = subprocess.Popen(
        [
            'pandoc',
            '--citeproc',
            '-M', 'reference-section-title=References',
            '--filter', 'filters/resolve-ref.py',
            '--filter', 'filters/eqn-no.py',
            *sys.argv[1:]
        ],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )

    out, err = process.communicate()
    if out:
        sys.stdout.write(out)
    if err:
        sys.stderr.write(err)


if __name__ == "__main__":
    main()
