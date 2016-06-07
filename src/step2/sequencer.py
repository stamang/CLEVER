# extractor.py uses CLEVER's terminology and note header file to generate generate concept sequences and other annotated textual information for expressing CLEVER rules for automatically labeling events documented in clinical text.
# input: file paths to the tagging lexicon with word class mappings, the list of clinical note headers, target classes for event extraction, maximum snippet length, directory path to the clinical corpus, number of workers, output folder and size of n-gram context for n-gram feature generation
# output: for target mentions detected using a maximum string length, right truncated partial string matching, CLEVER's output files include right and left n-gram features (context_left.txt, context_right.txt), candidate event snippets that can be used for additional processing steps such as SNOMED-CT concept extraction (discover.txt), and CLEVER's extraction files (extraction.txt). 
# *** it is important to note that only the extraction.txt file is required to develop a rule based extractor.  Additional textual features are provided in the extraction.txt file, and other extractor.py output; however, they are inteded to be used in the development of statistical extractors trained on a small portion of development data that is labeled by CLEVER during rule execution

import pdb
import sys
import codecs
from collections import defaultdict
import re
import os
import time
from argparse import ArgumentParser
from multiprocessing import Pool,Queue,Process
import Queue as qmod
from os import listdir
from os.path import isfile, join


reload(sys)
sys.setdefaultencoding('utf-8')

END_TOKEN = set(["."," ","?","!","\\","/","-"])

def read_headers(f):
    header_list = set()
    with codecs.open(f,"r","utf-8") as f:
        for line in f:
            header = line.strip().lower()
            if header:
                header_list.add(header)
        return header_list

def read_dict(f):
    terms = []
    with codecs.open(f,"r","utf-8") as f:
        for line in f:
            _id,label,_class = line.strip().split("|")
            term = Term(_id,label,_class)
            terms.append(term)
        return terms

class Term:
    def __init__(self,_id,label,_class):
        self._id = _id
        self.label = label
        self._class = _class

class NoteExtraction:
    def __init__(self,note):
        self.note = note
        self.targets = []

    def only_longest_targets(self):
        longest = []
        for target_a in self.targets:
            is_longest = True
            for target_b in self.targets:
                if target_a == target_b:
                    continue
                if target_a.is_contained_in(target_b):
                    is_longest = False
                    break
            if is_longest:
                longest.append(target_a)
        self.targets = sorted(longest,key=lambda x: x.offset)

    def add_target(self,target):
        self.targets.append(target)

    def any_targets(self):
        return len(self.targets) > 0

    def match_headers(self,headers):
        max_target = max(map(lambda x: x.offset,self.targets))
        header_text_space = self.note.text[:max_target]
        header_index = list()
        for header in headers:
            index = [m.start() for m in re.finditer(header+":",header_text_space)]
            for i in index:
                header_index.append((i, header))
        header_index = sorted(header_index,key=lambda x: x[0])
        for target in self.targets:
            for (i,header) in header_index:
                if i>target.offset:
                    break
                else:
                    target.header = (i,header)

    def dump(self,out_extraction,out_discover,snippets,ngram_contexts):
        sorted_targets = sorted(self.targets,key=lambda x: x.offset)
        lefts,rights = [],[]
        for i,target in enumerate(sorted_targets):
            left,right = target.dump(i,out_extraction,out_discover,snippets)
            lefts.append(left)
            rights.append(right)
        return lefts,rights

class MainTargetHit:
    def __init__(self,note,offset,size_context,term,context_terms):
        self.note = note
        self.offset = offset
        self.size_context = size_context
        self.term = term
        self.lsnip,self.rsnip = self.extract_target_snips()
        self.context_terms = context_terms
        self.context_hits=[]
        self.top_offset = self.offset + len(self.term.label)
        self.header = None

    def dump(self,i,out_extraction,out_discover,snippets):
        header_str = ""
        if self.header:
            header_str = "%s:%s"%(self.header[1],self.header[0])
        line = [self.note._id,"%s:%s"%(self.term._class,self.term._id),
                str(self.offset),header_str]
        context_sorted = sorted(self.context_hits,key=lambda x: x[2])
        for (offset,term,distance) in context_sorted:
            line.append("%s:%s:%d:%s"%(term._class,term._id,offset,distance))
        if snippets:
            line.append(self.note.text[self.linit:self.rend])
        out_extraction.write("\t".join(line)+"\n")
        left_context = self.note.text[self.linit:self.offset+len(self.term.label)]
        rigth_context = self.note.text[self.offset:self.rend]
        out_discover.write("[[ID=%s:%s:L]]\n"%(self.note._id,str(i)))
        out_discover.write(left_context + "\n")
        out_discover.write("[[ID=%s:%s:R]]\n"%(self.note._id,str(i)))
        out_discover.write(rigth_context+ "\n")
        #return context without the labels
        left = self.note.text[self.linit:self.offset]
        right = self.note.text[self.offset+len(self.term.label):self.rend]
        return left,right

    def is_contained_in(self,other):
        return other.offset <= self.offset and other.top_offset >= self.top_offset

    def extract_target_snips(self):
        ltext = len(self.note.text)
        linit = self.offset - self.size_context
        rend = self.offset + len(self.term.label) +  self.size_context
        if linit < 0:
            linit = 0
        if rend >= ltext:
           rend = ltext
        self.linit = linit
        self.rend = rend
        l = self.note.text[linit:self.offset]
        r = self.note.text[self.offset+len(self.term.label):rend]
        return l,r

    def add_context(self,term,hit,side):
        if side == 0: #left
            note_offset = self.offset - (len(self.lsnip) - hit)
        else: #right
            note_offset = self.offset + hit + len(self.term.label)
        distance = note_offset - self.offset
        self.context_hits.append((note_offset,term,distance))

    def only_longest_context(self):
        longest = []
        for context_a in self.context_hits:
            (note_offset,term,distance) = context_a
            top_offset = note_offset + len(term.label)
            is_longest = True
            for context_b in self.context_hits:
                if context_a == context_b:
                    continue
                if context_b[0] <= note_offset:
                    (note_offset_b,term_b,distance_b) = context_b
                    top_offset_b = note_offset_b + len(term_b.label)
                    if top_offset_b >= top_offset:
                        is_longest = False
                        break
            if is_longest:
                longest.append(context_a)
        self.context_hits = sorted(longest,key=lambda x: x[0])

    def extract_context_terms(self):
        for i,snip in enumerate([self.lsnip,self.rsnip]):
            snip_lower = snip.lower()
            for term in self.context_terms:
                offset = 0
                lt = len(term.label)
                ls = len(snip)
                while True:
                    hit = snip_lower.find(term.label,offset)
                    if hit == -1:
                        break
                    if hit+lt+1 < ls:
                        if snip[hit+lt] not in END_TOKEN:
                            break
                    self.add_context(term,hit,i)
                    offset = hit+len(term.label)
        if not args.include_shorter:
            self.only_longest_context()

class Note:
    def __init__(self,_id,text):
        self._id = _id
        self.text = text
        self.text_lower = text.lower()

    def extract(self,main_terms,context_terms,size_context,headers):
        nt = NoteExtraction(self)
        for term in main_terms:
            offset = 0
            while True:
                hit = self.text_lower.find(term.label,offset)
                if hit == -1:
                    break
                if self.text[hit+len(term.label)] not in END_TOKEN:
                    break
                target = MainTargetHit(self,hit,size_context,term,context_terms)
                target.extract_context_terms()
                nt.add_target(target)
                offset = hit+len(term.label)
        if nt.any_targets():
            nt.match_headers(headers)
            if not args.include_shorter:
                nt.only_longest_targets()
            return nt
        return None

def extract_context(words,start,end):
    words = filter(lambda x : len(x) > 0,words)
    step = 1
    if start > end:
        step = -1
    context = []
    for i in range(start,end,+1):
        if i > -1 and i < len(words):
            context.append(words[i])
        else:
            break
    context = " ".join(context).lower()
    return context

class NGramContext:
    def __init__(self,left_size,right_size):
        self.left_size = left_size
        self.right_size = right_size

    def dump_contexts(self,lefts,rights,fleft,fright):
        #left and right do not include the target label
        if self.left_size:
            for left in lefts:
                words = left.strip().split(" ")
                words = filter(lambda x: len(x) > 0, words)
                start = len(words)
                lcontext = extract_context(words,
                        start - self.left_size,start)
                fleft.write(lcontext + "\n")
        if self.right_size:
            for right in rights:
                words = right.strip().split(" ")
                words = filter(lambda x: len(x) > 0, words)
                rcontext = extract_context(words, 0, self.right_size)
                fright.write(rcontext + "\n")

    def aggregate(self,output_folder):

        onlyfiles = [join(output_folder,f) for f in listdir(output_folder)\
                if isfile(join(output_folder, f))]
        count_left = defaultdict(lambda : 0)
        count_right = defaultdict(lambda : 0)
        for f in onlyfiles:
            d = None
            if "context-left" in f:
                d = count_left
            elif "context-right" in f:
                d = count_right
            else:
                continue
            with open(f) as fin:
                for line in fin:
                    d[line.strip()] += 1
        self.dump_stats(join(output_folder,"context-left-stats.tsv"),count_left)
        self.dump_stats(join(output_folder,"context-right-stats.tsv"),count_right)


    def dump_stats(self,fname,counts):
        total = float(sum(counts.values()))
        accumulative = [(f,c,(float(c)/total) * 100) for (f,c) in counts.items()]
        sorted_acc = sorted(accumulative,key=lambda x: x[1],reverse=True)
        with open(fname,"w") as fout:
            fout.write("\n".join(map(lambda x: "%s\t%d\t%.4f"%
                (x[0],x[1],x[2]), sorted_acc)))

def process_note(line,offset_size,snippets,headers,
        main_terms,context_terms):
    parts = line.split("\t")
    if len(parts) == 1:
        return
    _id = parts[0]
    text = " ".join(parts[1:])
    note = Note(_id,text)
    note_extraction = note.extract(main_terms,context_terms,offset_size,headers)
    return note_extraction

class ExitProcess:
	pass

class Batch:
    def __init__(self,queue,snippet_length,snippets,
            headers,main_terms,context_terms,output_folder,ngram_contexts):
        self.queue = queue
        self.snippet_length= snippet_length
        self.snippets = snippets
        self.headers = headers
        self.main_terms = main_terms
        self.context_terms = context_terms
        self.output_folder = output_folder
        self.ngram_contexts = ngram_contexts

        if isinstance(self.queue,basestring):
            self.notes_file = open(self.queue,"r")

    def next_batch(self):
        if not isinstance(self.queue,basestring):
            try:
                batch = queue.get(True)
                if isinstance(batch,ExitProcess):
                    return None
                return batch
            except qmod.Empty:
                print("qmod empty")
                return []
        else:
            if self.notes_file == None:
                return None
            batch = []
            for line in self.notes_file:
                batch.append(line.strip())
            self.notes_file = None
            return batch

    def process(self):
        if isinstance(self.queue,basestring):
            pid = 0
        else:
            pid = os.getpid()
        output_file = codecs.open(
            os.path.join(self.output_folder,"extraction-%d.tsv"%pid),
            "w",encoding='utf8')
        discover_file = codecs.open(
            os.path.join(self.output_folder,"discover-%d.tsv"%pid),
            "w",encoding='utf8')
        fcontext_left = codecs.open(
            os.path.join(self.output_folder,"context-left-%d.tsv"%pid),
            "w",encoding='utf8')
        fcontext_right = codecs.open(
            os.path.join(self.output_folder,"context-right-%d.tsv"%pid),
            "w",encoding='utf8')

        while True:
            try:
                batch = self.next_batch()
                if batch is None:
                    return
                for line in batch:
                    ext = process_note(line,self.snippet_length,
                            self.snippets,headers,
                            self.main_terms,self.context_terms)
                    if ext:
                        lefts,rights = ext.dump(output_file,
                                discover_file,self.snippets,self.ngram_contexts)
                        if self.ngram_contexts:
                            ngram_contexts.dump_contexts(lefts,rights,
                                    fcontext_left,fcontext_right)
            except Exception,e:
                print(e)
                continue

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-o", "--output", dest="output_folder", default=None,
                        help="output folder", metavar="FILE")
    parser.add_argument("-n", "--notes", dest="notes_file", default=None,
                        help="Notes file", metavar="FILE")
    parser.add_argument("-l", "--lexicon", dest="lexicon", default="mbc-dic.txt",
                        help="read word classes from FILE", metavar="FILE")
    parser.add_argument("-w", "--workers", dest="workers", default=2,
                        metavar="N")
    parser.add_argument("-s", "--section-headers", dest="section_headers",
                        default="headers.txt", help="read headers from FILE",
                        metavar="FILE")
    parser.add_argument("-t", "--main-targets", dest="main_targets",
                        action="append", default=[],
                        help=("the word classes to use as a main target "
                              "(can be used multiple times)"),
                        metavar="TARGET")
    parser.add_argument("-ln", "--snippet-length",
            dest="snippet_length", type=int, default=150)
    parser.add_argument('--snippets', dest='snippets', action='store_true')
    parser.add_argument('--shorter-too', dest='include_shorter', action='store_true',
            default=False)
    parser.add_argument('--no-snippets', dest='snippets',  action='store_false')
    parser.add_argument('--left-gram-context', dest='left_gram',default=3)
    parser.add_argument('--right-gram-context', dest='right_gram',default=2)
    args = parser.parse_args()
    args.workers = int(args.workers)

    if not args.output_folder:
        print("Output folder must be provided with -o/--output")
        sys.exit(-1)
    if os.path.exists(args.output_folder):
        print("Output folder '%s' already exists"%(args.output_folder))
        print("This tool will create an empty folder to save clean data")
        sys.exit(-1)

    os.mkdir(args.output_folder)
    main_targets_index = set(["MBC","METS","BCTRIG"])
    if len(args.main_targets) > 0:
        main_targets_index = set(map(lambda x: x.strip(),
            args.main_targets[0].split(",")))

    terms = read_dict(args.lexicon)
    headers = read_headers(args.section_headers)

    main_terms = filter(lambda x: x._class in main_targets_index,terms)
    context_terms = filter(lambda x: x._class not in main_targets_index,terms)
    if len(main_terms) == 0:
        sys.stderr.write("Main targets not found - exiting")
        sys.exit(-1)

    if not args.snippets and (args.right_gram > 0 or args.left_gram > 0):
        sys.stderr.write(("If snippets are disabled context "
                          "ngrams cannot be extracted"))
        sys.exit(-1)
    ngram_contexts = None
    if args.left_gram:
        args.left_gram = int(args.left_gram)
    if args.right_gram:
        args.right_gram = int(args.right_gram)

    if args.snippets and (args.right_gram > 0 or args.left_gram > 0):
        ngram_contexts = NGramContext(args.left_gram,args.right_gram)

    if args.workers > 0:
        queue = Queue(args.workers)
        batch = Batch(queue,args.snippet_length,args.snippets,
                    headers,main_terms,context_terms,args.output_folder,
                    ngram_contexts)
        pool = Pool(args.workers,batch.process)

        batch = []
        with open(args.notes_file,"r") as file_notes:
            for line in file_notes:
                if len(batch) == 5000:
                    queue.put(batch,True,None)
                    batch = []
                batch.append(line.strip())
            if batch:
                queue.put(batch,True,None)

        time.sleep(60)
        for x in range(args.workers):
            queue.put(ExitProcess())
        queue.close()
    else:
        batch = Batch(args.notes_file,args.snippet_length,args.snippets,
                    headers,main_terms,context_terms,args.output_folder,
                    ngram_contexts)
        batch.process()


    if ngram_contexts:
        ngram_contexts.aggregate(args.output_folder)
