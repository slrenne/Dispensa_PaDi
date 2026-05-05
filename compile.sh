#!/bin/bash
FILENAME="main"

pdflatex "$FILENAME.tex" &&
bibtex "$FILENAME" &&
pdflatex "$FILENAME.tex" &&
pdflatex "$FILENAME.tex"

rm main.{aux,log,bbl,blg,bcf,run.xml,out,lof,toc}