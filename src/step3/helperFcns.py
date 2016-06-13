import glob

def loadSeqs(seqFiles,noteDict,mbcDict):
    sid = 0
    ants = {}
    for name in glob.glob(seqFiles):
        print name
        fin = open(name,"r")
        for line in fin:
            tags = []
            tmp_tags = []
            tag_offests = []
            sem = 0
            line = line.strip()
            tmp = line.split("\t")
            cols = len(tmp)
            nid = tmp[0].strip()
            if nid not in noteDict: continue
            sid += 1
            mdata = noteDict[nid]
            pid = mdata[0]
            doc_dec = mdata[1]
            tage = float(mdata[2])/365
            age = str(tage)
            nyear = mdata[3]            
            snippet = tmp[cols-1].strip()
            tmpt = tmp[1].split(":")
            tclass = tmpt[0]
            ttid = tmpt[1]
            tmpterm = mbcDict[ttid]
            tterm = tmpterm[0]
            tpos = tmp[2]
            if cols < 4: continue
            if sem != 1:
                tmpTestHead = tmp[3].split(":")
                if tmpTestHead[0].islower() and tmpTestHead != "": 
                    htmp = tmp[3].split(":")
                    head = htmp[0]
                    hpos = htmp[1]
                    if cols>5: tmptags = tmp[4:cols-1]
                    else: tmptags = []
                else:
                    head = "UK"
                    hpos = "NULL"
                    tmptags = tmp[4:cols-1]
            tmp_key = "S-"+str(sid)+"-"+tclass
            #testing print
            #print ""
            if tmptags == []:
                tmpstr="NONE"
                tagseqs = ["NONE","NONE"]
            else:
                tagterm = gettagterm(tmptags[0],mbcDict)
                tmpstr = tagterm
                if len(tmptags) > 1:
                    for i in range(1,len(tmptags)):
                        tmp_item = tmptags[i]
                        tagterm = gettagterm(tmp_item,mbcDict)
                        tmpstr = tmpstr+","+tagterm
                tagseqs = getTagseq(tmpstr,"125",tclass)
            truncseq = tagseqs[1]
            fullseq = tagseqs[0]
            sinfo = tmp_key+"|"+truncseq+"|"+fullseq+"|"+tterm+"|"+pid+"|"+nid+"|"+doc_dec+"|"+age+"|"+nyear+"|"+tclass+"|"+ttid+"|"+tpos+"|"+head+"|"+hpos+"|"+tmpstr+"|"+"SNIPPET: "+snippet
            #print tmp_key+"|"+tterm+"|"+pid+"|"+nid+"|"+doc_dec+"|"+age+"|"+nyear+"|"+tclass+"|"+ttid+"|"+tpos+"|"+head+"|"+hpos+"|"+tmpstr+"|"+snippet
            #print tagseqs
            #print sinfo
            #print tmptags
            #print tmp
            ants[tmp_key] = sinfo
    print len(ants),"total targets"
    return ants

def gettagterm(tag,dictionary):
    tmp = tag.split(":")
    tterm = dictionary[tmp[1]]
    tmpt = tterm[0].strip()
    if tmpt==":": tterm[0] = "colon"
    if tmpt==".": tterm[0] = "period"
    if tmpt=="/": tterm[0] = "slash"
    if tmpt==",": tterm[0] = "comma"
    taginfo = tterm[0]+":"+tag
    #print tag, taginfo
    return taginfo


def getTagseq(taginfo,window,tclass):
    wmax = int(window)
    wmin = -wmax
    fullseq = ""
    truncseq = ""
    tmptags = taginfo.split(",")
    #print "TAGINFO:",taginfo
    sem = 0
    #print "----------------------"
    for tag in tmptags:
        tmp = tag.split(":")
        tmpclass = tmp[1]
        tmppos = int(tmp[4])
        #print "TPOS:",str(tmppos),tmpclass
        if tmppos < 0:
            if fullseq == "": 
                fullseq = tmpclass
            else: 
                fullseq = fullseq+"_"+tmpclass
            if abs(tmppos) <= wmax:
                #print "good",truncseq
                if truncseq == "":
                    truncseq = tmpclass
                else: 
                    truncseq = truncseq+"_"+tmpclass
        if tmppos > 0 and sem == 1:
            fullseq = fullseq+"_"+tmpclass
            if tmppos <= wmax:
                truncseq = truncseq+"_"+tmpclass
        if tmppos > 0 and sem == 0:
            if fullseq == "":
                fullseq = "#"+tclass+"#"+"_"+tmpclass
            else:
                fullseq = fullseq+"_"+"#"+tclass+"#"+"_"+tmpclass
            if truncseq == "":
                truncseq = "#"+tclass+"#"+"_"+tmpclass
            else:
                truncseq = truncseq+"_"+"#"+tclass+"#"+"_"+tmpclass
            sem = 1
    #print fullseq, truncseq
    #print tag, taginfo                                                                                                                   
    return [fullseq,truncseq]


def getTerminology(dictname):
    termDict = {}
    print dictname
    with open(dictname) as f:
        for line in f:
            tmp = line.split("|")
            tid = tmp[0].strip()
            term = tmp[1].strip()
            tclass = tmp[2].strip()
            termDict[tid]=[term,tclass]
    return termDict
        

#loads all note metadata for patient subset
def loadSelectNoteMetadata(ptList):
# patient_id|note_id|doc_description|age_at_note_DATE_in_days|note_year        
    print "processing notemetadata for ",str(len(ptList)), " patients"
    fname = "/data3/stride6/tp_annotator_notes.txt"
    noteDict = {}
    fout_notemeta = open("/data3/mbc/notemetadata.txt","w")
    with open(fname) as f_in:
        for line in nonblank_lines(f_in):
            tmp = line.split("|")
            pid = tmp[0].strip()
            nid = tmp[1].strip()
            if pid in ptList:
                print >> fout_notemeta, line.strip()
#                with open("/data3/S6/corpus/notes/"+nid) as onconote:
#                    fout = open("/data3/oncoshare/oncocorpus/"+nid,"w")
#                print >> fout, onconote
                #fout.close()
                noteDict[tmp[1]]=[tmp[0],tmp[2],tmp[3],tmp[4]]
    print "Total notes: ",len(noteDict)
    return noteDict


def loadOncoNoteMdata(fname):
# patient_id|note_id|doc_description|age_at_note_DATE_in_days|note_year 
    noteDict = {}
    with open(fname) as f_in:
        for line in nonblank_lines(f_in):
            tmp = line.split("|")
            noteDict[tmp[1]]=[tmp[0],tmp[2],tmp[3],tmp[4]]
    print "Total notes: ",len(noteDict)
    return noteDict 


#loads all note metadata for STRIDE6
def loadNoteMetadata():
# patient_id|note_id|doc_description|age_at_note_DATE_in_days|note_year
    fname = "/data3/stride6/tp_annotator_notes.txt"
    noteDict = {}
    with open(fname) as f_in:
        for line in nonblank_lines(f_in):
            tmp = line.split("|")
            noteDict[tmp[1]]=[tmp[0],tmp[2],tmp[3],tmp[4]]
    print "Total notes: ",len(noteDict)
    return noteDict

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# pt list is a selected group of patients
# set ptList =0 to return all patients
def getS6ids(ptList,oncoKey):
    lc = 0
    oncoS6map = {}
    with open(oncoKey) as f_in:
        for line in nonblank_lines(f_in):
            if lc == 0: 
                lc += 1
                continue
            line = line.strip()
            tmp = line.split("\t")
#            print tmp
            if hasNumbers(tmp) == False: continue
            id_onco = tmp[0].strip()
            id_S6 = tmp[1].strip()
            #print id_onco,id_S6
            oncoS6map[id_onco]=id_S6
            #print oncoS6map[id_onco]
    f_in.close()
#    print oncoS6map
    #print oncoS6map[2933]
    sample = {}
    if ptList == 0:
        print "Total pts:", len(oncoS6map)
        return oncoS6map
    with open(ptList) as f_in:
        for line in nonblank_lines(f_in):
            tmp = line.strip()
            id_onco = tmp
            x = oncoS6map[id_onco]
            sample[tmp]=x
    print "Total Sampled pts:", len(sample)
    return sample

