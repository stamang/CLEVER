# CLEVER #
##(CL-inical EVE-nt R-ecognizer)##

This documentation walks through an application of CLEVER for quality measurement event detection.  Specifically, the automatic extraction of Physicain Quality Reporting System measures.  Draft paper can be found here: https://www.dropbox.com/s/f10szg57rhpt1fg/quality_measures_egems.docx?dl=0

##Application: Quality Measurement Event Detection###

##Step 1: Terminology Construction##
```
Directory: CLEVER/res/w2v/
Source: clinicalphrasesv1.sh
```
Bash code for normalizing the clinical corpus and training word and phrase embeddings, using a cbow model and the word2vec's source code.

##Step 2: Preprocessing##
```
Directory: CLEVER/src/
Source: extractor.py
```
**Corpus:** 
CLEVER/res/corpus/
Location of clinical notes directory; each note in the directory should appear on one line, preceded by the note identifier and a tab character.  For example:
```
11008624	 history: the patient returns today for followup of left maxillary sinus 
```
**extractor.py** uses the corpus (formatted as indicated above), CLEVER's terminology and note header file to extract concept sequences and other annotated information from clinical text.  The output of the extractor can be be used to design CLEVER rules for clinical event detection tasks.                  
 
###Get Targets###
```
Directory: CLEVER/src/
Source: getTargets.py [targetwordclass(es)]
Dependency: helperFcns.py
```
##Step 3: Extraction##
```
Directory: CLEVER/src/
Source: executer.py 
Dependency: ruleFcns.py
```
##Step 4: Patient-level Reporting##
```
Directory: CLEVER/src/
Source: getCleverXPt.py 
Dependency: helperFcns.py
```
#Resources#
##Terminology##
CLEVER/res/dicts/mbc_terminology.txt
###Section headers###
CLEVER/res/headers.txt







