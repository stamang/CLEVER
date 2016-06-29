import os, sys, operator
from step3fcn import *

# must rpovide the dict file and the project name
dictfile = sys.argv[1]
proj = sys.argv[2]
ppath = "../../proj/"+proj+"/"
ptKey = "../../proj/"+proj+"/ptselection/ptkey.txt"  
noteMdata = "../../res/corpus/testnotemdata.txt"
# target classes #
target_class = ["mbc","drecur","lrecur","loco","mets"]
s6pts = getPids(0,ptKey)                                             #S6 ids for subset
termDict = getTerminology(dictfile)                                          #get terminology

#for pt in s6pts: print pt,s6pts[pt]
noteMDict = loadOncoNoteMdata(noteMdata)                                     #patient_id|note_id|doc_description|age_at_note_DATE_in_days|note_year

seqDict = {}
for target in target_class:
    seqFile = ppath +"ants/"+target+"/extraction*.tsv"
    tmpDict = loadSeqs(seqFile,noteMDict,termDict)
    seqDict.update(tmpDict)
print len(seqDict)

for oncoid in s6pts:
    pt = str(s6pts[oncoid])
#for pt in testpts:
#    print pt
    ptAnts = []
    fout = open(ppath+"/ptseq/seqs_"+pt+".txt","w") 
    for sid in seqDict:
        tmp = seqDict[sid]
        sinfo = tmp.split("|")
        #print sinfo
        tmpsinfo = sinfo[0].split("-")
        if tmpsinfo[1]==pt:
            #print "found:",sinfo
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
