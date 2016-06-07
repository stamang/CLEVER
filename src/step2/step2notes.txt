1) In the project directory, create output directories for each of the target classes.  For example, the pqrs anntotation output directories are located here: /proj/pqrs/

Run the CELVER sequencer.  The example below targets the "DEM" class and writes annotations to the /proj/pqrs/dem output directory for further processing.

> python sequencer.py --lexicon ../../res/dicts/clever_terminology.txt --section-headers ../../res/headers.txt --main-targets DEM --snippet-length 125 --snippets --notes ../../res/corpus/testnotes_formatted.txt --workers 2 --output /proj/pqrs/dem --left-gram-context 3 --right-gram-context 2

2) Optional: getTargets.py can be used to collect target terms for a select sample of patients and uses helperFcns.py
