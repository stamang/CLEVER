import os, sys
from helperFcns import *

version = "V3"
path = "/data3/mbc"                                                          #mbc path
#mbcPts = path+"/validation/prelim/mbctest.txt"                               #select patients
oncoKey = path+"/oncoshare/oncoshare_s6_map.txt"                             #oncoshare-S6 map
noteMdata = path+"/notemetadata.txt"
dictfile = "/data3/clever/mbc/mbc-dic_"+version+".txt"
#dictfile = "/data3/mbc/src/clever/mbc-dic.txt"

# main #
#target_class = ["mbc_class"]
target_class = ["mbc_class","drecur_class","mets_class","lrecur_class"]
s6pts = getS6ids(0,oncoKey)                                             #S6 ids for subset
termDict = getTerminology(dictfile)                                          #get terminology

for key in s6pts: print key,s6pts[key]
noteMDict = loadOncoNoteMdata(noteMdata)                                     #patient_id|note_id|doc_description|age_at_note_DATE_in_days|note_year

for target in target_class:
    fout = open("/data3/clever/mbc/seq/"+version+"/seqs_"+target+".txt","w")
    seqFile = "/data3/clever/mbc/seq/"+version+"/"+target+"/extraction*.tsv"
    seqDict = loadSeqs(seqFile,noteMDict,termDict)
    for key in seqDict:
        print >> fout, key+"|"+seqDict[key]
    fout.close()
