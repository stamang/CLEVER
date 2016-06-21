import os, sys, operator
from helperFcns import *

proj = "pqrs"
ppath = "../../proj/"+proj+"/"
ptKey = "../../proj/"+proj+"/ptkey.txt"  
noteMdata = "../../res/corpus/testnotemdata.txt"
dpath = "../../res/dicts/"
dictfile = dpath+"clever_terminology.txt"
# target classes #
target_class = ["mbc","drecur","lrecur","advp","recur","mets"]
s6pts = getPids(0,ptKey)                                             #S6 ids for subset
termDict = getTerminology(dictfile)                                          #get terminology

#for pt in s6pts: print pt,s6pts[pt]
noteMDict = loadOncoNoteMdata(noteMdata)                                     #patient_id|note_id|doc_description|age_at_note_DATE_in_days|note_year

seqDict = {}
for target in target_class:
    seqFile = ppath +"seq/"+target+"/extraction*.tsv"
    print seqFile
    tmpDict = loadSeqs(seqFile,noteMDict,termDict)
    seqDict.update(tmpDict)
print len(seqDict)

for oncoid in s6pts:
    pt = str(s6pts[oncoid])
#for pt in testpts:
    print pt
    ptAnts = []
    fout = open(ppath+"/ptseq/seqs_"+pt+".txt","w") 
    for sid in seqDict:
        tmp = seqDict[sid]
        sinfo = tmp.split("|")
        print sinfo
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
