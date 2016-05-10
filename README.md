# CLEVER #
##(CL-inical EVE-nt R-ecognizer)##

This documeention walks through an application of CLEVER for quality measurement event detection.  Specifically, the automatic extraction of Physicain Quality Reporting System measures.

##Resources##
###Terminology##
CLEVER/res/dicts/mbc_terminology.txt
###Section headers###
CLEVER/res/headers.txt

##Applications##
###Quality Measurement Event Detection###
**Corpus:** 
CLEVER/res/corpus/
Location of clinical notes directory; each note in the directory should appear on one line, preceded by the note identifier and a tab character.  For example:
```
11008624	 history: the patient returns today for followup of left maxillary sinus 
```
##Step 1: Terminology Construction##
```
Directory: CLEVER/res/w2v/
Source: clinicalphrasesv1.sh
```
Bash code for normalizing the clinical corpus and training word and phrase embeddings, using a cbow model and the word2vec's source code.

##Step 2:Preprocessing##
```
Directory: CLEVER/src/
Source: extractor.py
```
**extractor.py** uses CLEVER's terminology and note header file to extract concept sequences and other annotated information from clinical text.  The output of the extractor can be be used to design CLEVER rules for clinical event detection tasks.                  

Example command line:
```
python extractor.py
--lexicon terminology.txt \
--section-headers headers.txt \
--main-targets MBC,DRECUR \
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

###Get Targets###
```
getTargets.py [targetwordclass(es)]
```
##Step 3: Extraction##
```
Directory: CLEVER/src/
executer.py 
```









