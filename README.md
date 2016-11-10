# Combine .tex

Python command line script to combine multiple .tex files into one.
This is intended to aid in the submission process where some journals
do not accept multiple tex files.

## Installation
```
pip install combine_tex
```

## Usage
```
combine-tex -i INPUTFILE -o OUTPUTFOLDER
```
`INPUTFILE` is the relative or absolute path to the main tex file.
`OUTPUTFOLDER` is the relative or absolute path to the desired output
folder.

## What it does
All `.tex` files will be combined into one tex file with the same name
as `INPUTFILE` and placed in the `OUTPUTFOLDER` directory.  Figures
well be copied and renamed to `f01.pdf`, `f02.pdf`, etc. and placed in the
`OUTPUTFOLDER` directory.  The `.tex` code will automatically be updated
to include these new figure names.

## Known Limitations
1. Only `.pdf` figures are supported
2. References need to be in a `references.bib` file in the same folder
as the input file.

## Changelog
### [0.1.0] - 2016-11-10
 - Initial Release