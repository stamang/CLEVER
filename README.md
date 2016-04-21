# CLEVER #
##(CL-inical EVE-nt R-ecognizer)##

##Step 1: Extract##
```
CLEVER/src/extractor.py
```
**extractor.py** uses CLEVER's terminology and note header file to extract concept sequences and other annotated information from clinical text.  The output of the extractor can be be used to design CLEVER rules for clinical event detection tasks.                  

Example command line:
```
python extractor.py
--lexicon terminology.txt \
--section-headers headers.txt \
--main-targets MBC,BCTRIG,METS \
--snippet-length 150 \
--snippets \
--notes /path/to/notes/file \
--workers 10 \
--output /path/to/output/folder \
--left-gram-context 3 \
--right-gram-context 2
```

**INPUT:** file paths to the tagging lexicon with word class mappings, the list of clinical note headers, target classes for event extraction, maximum snippet length, directory path to the clinical corpus, number of workers, output folder and size of n-gram context for n-gram feature generation     

**OUTPUT:** for target mentions detected using a maximum string length and right truncated exact string matching, CLEVER's output files include right and left n-gram features (context_left.txt, context_right.txt), candidate event snippets that can be used for additional processing steps (we use lexigram.io's Discover tool for concept recognition), and CLEVER's extraction files (extraction_processid.txt). 

##Target##
```
getTargets.py [targetwordclass(es)]
```
##Lablel##
```
CLEVER/src/executer.py 
```
##Terminology##
CLEVER/res/dicts/mbc_terminology.txt

##Applications##
###Quality Measurement Event Detection###
**Corpus:** 
CLEVER/res/corpus/
Location of clinical notes directory; each note in the directory should appear on one line, preceded by the note identifier and a tab character.








