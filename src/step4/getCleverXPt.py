import os, sys, operator
from helperFcns import *

version = "V6"
path = "/data3/mbc"                                                          #mbc path
oncoKey = path+"/oncoshare/oncoshare_s6_map.txt"                             #oncoshare-S6 map
noteMdata = path+"/notemetadata.txt"
#dictfile = "/data3/mbc/src/clever/mbc-dic.txt"
dictfile = "/data3/clever/mbc/mbc-dic_"+version+".txt"

#first neg, all else pos
testpts = ["1429499","1158149","1320506","298541","1429499","1619903","1838136","1523543"]

# main #
target_class = ["mbc_class","drecur_class","mets_class"]
s6pts = getS6ids(0,oncoKey)                                             #S6 ids for subset
termDict = getTerminology(dictfile)                                          #get terminology

#for pt in s6pts: print pt,s6pts[pt]
noteMDict = loadOncoNoteMdata(noteMdata)                                     #patient_id|note_id|doc_description|age_at_note_DATE_in_days|note_year

seqDict = {}
for target in target_class:
    seqFile = "/data3/clever/mbc/seq/"+version+"/"+target+"/extraction*.tsv"
    tmpDict = loadSeqs(seqFile,noteMDict,termDict)
    seqDict.update(tmpDict)
print len(seqDict)

for oncoid in s6pts:
    pt = str(s6pts[oncoid])
#for pt in testpts:
#    print pt
    ptAnts = []
    fout = open(path+"/oncoshare/clever/ptseq/"+version+"/seqs_"+pt+".txt","w") 
    for sid in seqDict:
        tmp = seqDict[sid]
        sinfo = tmp.split("|")
        #print sinfo
        if sinfo[4]==pt:
#            print "found"
            toff = sinfo[7]
            litem = [toff,tmp]
            if litem not in ptAnts:
                ptAnts.append(litem)
    ptList = sorted(ptAnts, key=operator.itemgetter(0))
    #tmpPtList = set(ptList)
    #ptList = list(tmpPtList)
    for item in ptList:
            #print item[0],item[1]
        print >> fout, item[1]
    fout.close()
