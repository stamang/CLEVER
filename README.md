# CLEVER #
##(CL-inical EVE-nt R-ecognizer)##

This documentation will walk you throught the installation of CLEVER and an the execution of our case study, which is an example of the application of CLEVER for quality measurement event detection.  More details on the application of CLEVER for quality measurement can be found in our [research paper][1].

#Resources#
##Terminology##
CLEVER/res/dicts/[clever_terminology.txt][2]

###Section headers###
CLEVER/res/[headers.txt][3]
Code for aggreagating and termporally ordering labeled events by patient

##Case study: Quality Measurement Event Detection###

##Step 1: Terminology Construction##

[Step 1 Wiki Page][4]
```
Directory: CLEVER/src/step1/
Source: clinicalphrases.sh, processMimic.py
```
Shell script is for for normalizing the clinical corpus and training word and phrase embeddings, using a cbow model and the word2vec's source code.

Python script processes the raw data file from the corpus directory "testnotes.txt" and generates a notemetadata file with patient id, note id, timestamp and note type information and another file, "testnotes_formatted.txt" with clinical notes formatted for Step 2.

##Step 2: Text Preprocessing##
[Step 2 Wiki Page][5]
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
[Step 3 Wiki Page][6]
```
Directory: CLEVER/src/
Source: executer.py 
Dependency: ruleFcns.py
```
Code for developing and executing CLEVER rules
##Step 4: Patient-level Reporting##
[Step 4 Wiki Page][7]
```
Directory: CLEVER/src/
Source: getCleverXPt.py 
Dependency: helperFcns.py
```

[1]: https://www.dropbox.com/s/f10szg57rhpt1fg/quality_measures_egems.docx?dl=0   "research paper"
[2]: https://github.com/stamang/CLEVER/blob/master/res/dicts/clever_terminology.txt "clever_terminology.txt"
[3]: https://github.com/stamang/CLEVER/blob/master/res/header.txt "header.txt"
[4]: https://github.com/stamang/CLEVER/wiki/Step-1:-Terminology-Construction "Step 1"
[5]: https://github.com/stamang/CLEVER/wiki/Step-2:-Text-Preprocessing "Step 2"
[6]: https://github.com/stamang/CLEVER/wiki/Step-3:-Extraction "Step 3"
[7]: https://github.com/stamang/CLEVER/wiki/Step-4:-Patient-level-Reporting "Step 4"







