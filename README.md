# RevTeX2docx

This repo includes wrapper scripts (currently implemented in [`just`][1] script) and [`pandoc` filters][2] to convert LaTeX files written (especially, in the RevTeX format) to docx files. In addition to `pandoc`'s built-in features, the filters and wrapper scripts are designed to handle the following:

* Cross-reference numbering for equations, figures, tables and titles: this is achieved by reading the `.aux` files generated at LaTeX compile time.
* Replacing unsupported LaTeX commands with their supported equivalents.

## Usage

Install the dependencies, including `pandoc`, `just`, a LaTeX distribution with `latexmk`, and Python packages `pandocfilters` and `texsoup` used by the filters.

Then drop the zipped LaTeX files as `src.zip` into this current folder and run the following command:

```bash
just src docx
```

This will unzip the `src.zip` file into the `src` folder, and convert the LaTeX files to docx files. The `docx_supp` target will also generate a supplementary docx file that includes the supplementary information files.

For additional targets, look into the `justfile` script.

## Known issues

Currently, some issues persists:

* The text replacements in the `just` script are performed with `sed`, the command is written in a way that works with the macOS's `sed` command around the use of `-i` flag. 
* The Equation numbering is not supported.
* The first paragraph after the equation, will always be indented.
* The affiliations are not supported.

## Roadmap

* Add tests and examples.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[1]: https://github.com/casey/just
[2]: https://pandoc.org/filters.html

