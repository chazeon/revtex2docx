
zip := 'src.zip'
bib := 'Geophysics.bib'
tex := 'main.tex'
csl := 'prb.csl'
ref_docx := 'main-ref.docx'
ref_docx_supp := 'supp-ref.docx'
ref_docx_letter:= 'letter-ref.docx'
docx := 'main.docx'
pdf := 'main.pdf'

src: clean
	unzip -d src {{zip}}
	sed -i '' 's/figure\*/figure/g' src/main.tex
	sed -i '' 's/SCFigure/figure/g' src/main.tex
	sed -i '' 's/table\*/table/g' src/main.tex
	sed -i '' 's/FIG\([0-9]*\)\.pdf/FIG\1.png/g' src/main.tex
	sed -i '' '/\\begin{minipage}/d' src/main.tex
	sed -i '' '/\\end{minipage}/d' src/main.tex
	sed -i '' '/\\raggedright/d' src/main.tex
	sed -i '' 's/\\begin{split}/\\begin{aligned}/g' src/main.tex
	sed -i '' 's/\\end{split}/\\end{aligned}/g' src/main.tex
	sed -i '' 's/\\hbox{}//g' src/main.tex
	sed -i '' 's/\\langle/\\left\\langle/g' src/main.tex
	sed -i '' 's/\\rangle/\\right\\rangle/g' src/main.tex
	sed -i '' 's/\\bigg//g' src/main.tex
	sed -i '' 's/\\big//g' src/main.tex
	sed -i '' 's/\\eqref{}/\\ref{}/g' src/main.tex
	sed -i '' -E 's/\\eqref{([^}]*)}/(\\ref{\1})/g' src/main.tex
	# cat src/main.tex | python3 move-floats.py > src/main.tex.tmp && mv src/main.tex.tmp src/main.tex

pdf: pdf2png
	cd src && \
	latexmk -pdflatex {{tex}}

pdf2png:
	for pdf_file in src/FIG*.pdf; do \
		png_file="${pdf_file%.pdf}.png" ; \
		[ ! -f "$png_file" ] && [ -f "$pdf_file" ] && mutool draw -o "$png_file" -r 300 "$pdf_file" ; \
	done
	
docx: pdf pdf2png 
	cd src && \
	pandoc {{tex}} \
	  --citeproc \
	  --bibliography={{bib}} \
	  -M reference-section-title=References \
	  --csl=../{{csl}} \
	  --reference-doc=../{{ref_docx}} \
	  --filter ../filters/fix-texmath.py \
	  --filter ../filters/resolve-ref.py \
	  -t json -o ../{{docx}}.json && \
	pandoc {{tex}} \
	  --citeproc \
	  --bibliography={{bib}} \
	  -M reference-section-title=References \
	  --csl=../{{csl}} \
	  --reference-doc=../{{ref_docx}} \
	  --filter ../filters/fix-texmath.py \
	  --filter ../filters/resolve-ref.py \
	  -t docx -o ../{{docx}}

docx_supp:
	cd src && \
	pandoc supp.tex \
	  --citeproc \
	  --bibliography={{bib}} \
	  -M reference-section-title=References \
	  --csl=../{{csl}} \
	  --reference-doc=../{{ref_docx_supp}} \
	  --filter ../filters/fix-texmath.py \
	  -t docx -o ../supp.docx

	## cp main.docx main-$(date +%Y%m%d%H%M).docx

docx_letter:
	cd src && \
	pandoc correspondence/submission.tex \
	  --reference-doc=../{{ref_docx_letter}} \
	  -t docx -o ../submission.docx

	## cp main.docx main-$(date +%Y%m%d%H%M).docx

all: pdf docx

clean:
	rm -rf src
	rm -f {{docx}}
