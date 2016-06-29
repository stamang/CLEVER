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
#	print "LABEL: ", label
	#print tmp
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
#	print lseq,rseq
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
#				print "NEG: ",tag,tclass,cseq
				return [neg,tag] 
		if lrseq > 0:
			post1 = rseq[0]
			if post1 == tag: 
#				print "NEG: ",tag,tclass, cseq
				return [neg,tag]
		# two to the left, look for salvage before retuning value
		if llseq > 2:
			pre2 = lseq[llseq-2]
			if pre2 == tag and pre1 != "DOT": 
#				print "NEG: ",tag,tclass,cseq
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
#	exception = 1
	#for tag in trigs:
	#	if cseq[0] != None and cseq[1] != None:
	#		if (tag not in lseq and tag not in rseq):
	#			if ("BLOC"in cseq[0] or "BLOC" in cseq[1]) or ("DRECUR" in cseq[0] or "DRECUR" in cseq[1]):
	#				print "POS: ","DRECUR_P",tclass,cseq
	#				esem = "-E2"
	#			else: exception = 0
	#		else: exception = 0
	#	elif cseq[0] == None:
	#		if (tag not in cseq[1]):
        #                        if ("BLOC"in cseq[1]  or "DRECUR" in cseq[1]):
        #                                print "POS: ","DRECUR_P",tclass,cseq
	#				esem = "-E3"
	#			else: exception = 0
	#		else: exception = 0
	#	elif cseq[1] == None:
	#		if (tag not in cseq[0]):
	#			if ("BLOC"in cseq[0]  or "DRECUR" in cseq[0]):
        #                                print "POS: ","DRECUR_P",tclass,cseq
	#				esem = "-E4"
	#			else: exception = 0
	#		else: exception = 0
	#if exception == 1: return [pos,"DRECUR_P"+esem]

#	print "POS: ",tclass,cseq
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
fout_pos = open(opath+"all_pos.txt","w")
fout_neg = open(opath+"all_neg.txt","w")
fout_drecur = open(opath+"all_drecur.txt","w")
for fin in fins:
	print fin
	tmp = fin.strip(".txt")
	tmp = tmp.split("_")
#	print tmp
	tmpf = "pt"+tmp[1]
#	print "PT:",tmpf
	fpos = open(opath+tmpf+"_pos.txt","w")
	fneg = open(opath+tmpf+"_neg.txt","w")
	fcron = open(opath+tmpf+"_cron.txt","w")
#	print "\n"
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
#			print label, tmp
			sum_out = label[0]+"|"+label[1]+"|"+pid+"|"+year+"|"+cid+"|"+time+"|"+ntype+"|"+nid+"|"+tterm+"|"+snippet
			long_out =  label[0]+"|"+label[1]+"|"+tmp
			if label[0] == "POSITIVE":
				print >> fout_pos, long_out
				print >> fpos, sum_out
				print >> fcron, sum_out
		                if "DRECUR" in label[1]:
                                     print >> fout_drecur, sum_out
                        if label[0] == "NEGATIVE":
                                print >> fout_neg, long_out
				print >> fneg, sum_out
				print >> fcron,sum_out
	fpos.close()
	fcron.close()
	fneg.close()

fout_pos.close()
fout_neg.close()

#s =assignMBCLabel(snippet)
#print s

#s = assignMBCLabel(s2)
