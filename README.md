# CLEVER #
##(CL-inical EVE-nt R-ecognizer)##

I get 10 times more traffic from [Google][1] than from
[Yahoo][2] or [MSN][3].

[1]: http://google.com/        "Google"
[2]: http://search.yahoo.com/  "Yahoo Search"
[3]: http://search.msn.com/    "MSN Search"

This documentation will walk you throught the installation of CLEVER and an the execution of our case study, which is an example of the application of CLEVER for quality measurement event detection.  Specifically, the automatic extraction of ten Physicain Quality Reporting System measures described our [research paper][1].

#Resources#
##Terminology##
[CLEVER/res/dicts/clever_terminology.txt][2]

###Section headers###
[CLEVER/res/headers.txt][3]
Code for aggreagating and termporally ordering labeled events by patient

##Case study: Quality Measurement Event Detection###

##Step 1: Terminology Construction##

[Step 1 wiki page][4]
```
Directory: CLEVER/src/step1/
Source: clinicalphrases.sh, processMimic.py
```
Shell script is for for normalizing the clinical corpus and training word and phrase embeddings, using a cbow model and the word2vec's source code.

Python script processes the raw data file from the corpus directory "testnotes.txt" and generates a notemetadata file with patient id, note id, timestamp and note type information and another file, "testnotes_formatted.txt" with clinical notes formatted for Step 2.

##Step 2: Text Preprocessing##
```
Directory: CLEVER/src/step2/
Source: sequencer.py
```
**Corpus:** 
CLEVER/res/corpus/testnotes.txt
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
Code for aggreagating and sorting target annotations for a preidentifed set of patients

##Step 3: Extraction##
```
Directory: CLEVER/src/
Source: executer.py 
Dependency: ruleFcns.py
```
Code for developing and executing CLEVER rules
##Step 4: Patient-level Reporting##
```
Directory: CLEVER/src/
Source: getCleverXPt.py 
Dependency: helperFcns.py
```

[1]: https://www.dropbox.com/s/f10szg57rhpt1fg/quality_measures_egems.docx?dl=0   "research paper"






