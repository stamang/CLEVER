Instructions for Step 1: Terminology Construction

1) process all notes so that each note appears on one line and is preceded by a tab caracter and the note identifier.

processNotes.py will transform the MIMIC notes to CELVER format:
clever/res/corpus/testnotes.txt -> clever/res/corpus/textnotes_formatted.txt

> cd clever/src/step1/
> python processMimic.py

2) build a word embedding model of the corpus that you can query to perfrom corpus-driven term expansion.  This is descriped as Step 1 in the CELVER framework, Terminology Construction.

> cd clever/res/embed/word2vec/
> make

*malloc.c is a non-standard header file and you may need to update the library to stdlib.c or remove it for compilation

To build a phrase ebedding model, compile word2vec and use the clinical_phrases.sh code to normalize the corpus and learn a nural language model of the corpus.

To run the model,

> cd clever/src/step1/word2vec
> ./distance vector-phrase.bin

3) Place your terminology here: clever/res/dicts

