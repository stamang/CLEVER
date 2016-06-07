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
