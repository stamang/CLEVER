import os, sys, glob

def assignMBCLabel(cevent):
	sem = 1
	tmp = cevent.split("|")
	sinfo = tmp[0].split("-")
	cid = sinfo[1]
	tclass = sinfo[2].strip()
	cseq = formatSeq(tmp[1],tclass)
	if cseq == [None,None] : 
		return ["POSITIVE",tclass]
	sentsem= checkSentence(cseq[0],cseq[1])
	if sentsem == 1: 
		return ["POSITIVE",tclass]
	label = cleverRule(cseq,tclass)
	return label 

def formatSeq(seq,tclass):
	lseq = None
	rseq = None
	if "_#"+tclass+"#_" in seq: 
		tmp = seq.split("_#"+tclass+"#_")
		lseq = tmp[0].split("_")
		rseq = tmp[1].split("_")
	elif "_#"+tclass+"#" in seq: 
		tmp = seq.split("_#"+tclass+"#")
		lseq = tmp[0].split("_")
	elif "#"+tclass+"#_" in seq: 
		tmp = seq.split("#"+tclass+"#_")
		rseq = tmp[1].split("_")
	return [lseq,rseq]

def cleverRule(cseq,tclass):
	pos = "POSITIVE"
	neg = "NEGATIVE"
	trigs = ["NEGEX","HYP","SCREEN","RISK","FAM","PREV"]
	if cseq[0] == None:
		llseq = 0
		pre1 = "DOT"
	else:
		lseq = cseq[0]
		llseq = len(cseq[0])
        if cseq[1] == None:
                lrseq = 0
		post1 = "DOT"
	else:
		rseq = cseq[1]
		lrseq = len(rseq)

	for tag in trigs:
		if llseq > 0: 
			pre1 = lseq[llseq-1]
			if pre1 == tag: 
				return [neg,tag] 
		if lrseq > 0:
			post1 = rseq[0]
			if post1 == tag: 
				return [neg,tag]
		if llseq > 2:
			pre2 = lseq[llseq-2]
			if pre2 == tag and pre1 != "DOT": 
				return [neg,tag]
                if llseq > 3 and tag != "NEGEX":
                        pre3 = lseq[llseq-3]
                        if pre3 == tag and pre1 != "DOT": 
				return [neg,tag] 
	#print "Probably POSITIVE, is it a DRECUR?"
	if tclass == "DRECUR": 
#		print "POS: ",tclass, cseq
		return [pos,tclass]
	if tclass != "DRECUR" and tclass != "LRECUR": #likely a positive, is at a drecurr?
		#if llseq > 3:
			#pre3 = lseq[llseq-3]
			#if pre3 == tag and pre1 != "DOT": return tag
                if lrseq> 2:
                        post2 = rseq[1]
			if (post1 == "BLOC" and post2 == "BLOC") or  (post1 == "LOC" and post2 == "BLOC") or  (post1 == "BLOC" and post2 == "LOC"):
#				print "POS: ","DRECUR_P",tclass,cseq
				return [pos,"DRECUR-E1"]
	return [pos,tclass]

def checkSentence(lseq,rseq):
	if lseq == None and rseq == None: 
		return 1
	elif lseq == None:
		if "DOT" == rseq[0]: 
			return 1
	elif rseq == None:
		if "DOT" == lseq[len(lseq)-1]: 
			return 1
	elif "DOT" == lseq[len(lseq)-1] and "DOT" == rseq[0]:
			return 1
	else: return 0

measure = "mbc"
proj = "pqrs"
ppath = "../../proj/"+proj+"/"
fins = glob.glob(ppath+"ptseq/seqs_*.txt")
opath = ppath+"labeled/"+measure+"/"
ptPEvents = {}
ptNEvents = {}
ptEvents = {}
fout_pos = open(opath+"all_pos.txt","w")
fout_neg = open(opath+"all_neg.txt","w")
fout_drecur = open(opath+"all_drecur.txt","w")
for fin in fins:
	print fin
	with open(fin) as f:
		for line in f:
			tmp = line.strip()
			label = assignMBCLabel(tmp)
			tmpe = tmp.split("|")
			cid = tmpe[0]
			tseq = tmpe[1]
			longseq = tmpe[2]
			tterm = tmpe[3]
			pid = tmpe[4]
			nid = tmpe[5]
			ntype = tmpe[6]
			time = tmpe[7]
			year = tmpe[8]
			tclass = tmpe[9]
			tags = tmpe[14]
			snippet = tmpe[len(tmpe)-1]
			sum_out = label[0]+"|"+label[1]+"|"+pid+"|"+year+"|"+cid+"|"+time+"|"+ntype+"|"+nid+"|"+tterm+"|"+snippet
			long_out =  label[0]+"|"+label[1]+"|"+tmp
                        tmpE = ""
			if label[0] == "POSITIVE":
				print >> fout_pos, long_out
                                if pid not in ptPEvents:
                                        ptPEvents[pid]=[sum_out]
                                        ptEvents[pid]=[sum_out]
                                else:
                                        tmpE = ptPEvents[pid]
                                        tmpE.append(sum_out)
                                        ptPEvents[pid]=tmpE
                                        ptEvents[pid]=tmpE
                                        print sum_out,tmpE
		                if "DRECUR" in label[1]:
                                     print >> fout_drecur, sum_out
                        if label[0] == "NEGATIVE":
                                print >> fout_neg, long_out
                                if pid not in ptNEvents:
                                        ptNEvents[pid]=[sum_out]
                                        ptEvents[pid]=[sum_out]
                                else:
                                        tmpE = ptNEvents[pid]
                                        tmpE.append(sum_out)
                                        ptNEvents[pid]=tmpE
                                        ptEvents[pid]=tmpE
                                        print sum_out,tmpE

fout_pos.close()
fout_neg.close()

print len(ptPEvents)
print len(ptNEvents)
print len(ptEvents)
for pid in ptPEvents:
        fpos = open(opath+"pt"+pid+"_pos.txt","w")
        te = ptPEvents[pid]
        for i in range(len(te)):
                tevent = te[i]
                print >> fpos,tevent
                print pid,tevent
        fpos.close()

for pid in ptNEvents:
        fneg = open(opath+"pt"+pid+"_neg.txt","w")
        te = ptNEvents[pid]
        for i in range(len(te)):
                tevent = te[i] 
                print >> fneg,tevent
                print pid,tevent
        fneg.close()

for pid in ptEvents:
        fcron = open(opath+"pt"+pid+"_cronology.txt","w")
        te = ptEvents[pid]
        for i in range(len(te)):
                tevent = te[i] 
                print >> fcron,tevent
                print pid,tevent
        fcron.close()

#s =assignMBCLabel(snippet)
#print s

#s = assignMBCLabel(s2)
