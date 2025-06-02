"""
Usage:
 txtfreq  [Options] files
 Options:
   -l        lemmas (default)
   -w        words
   -m 10     just the first 10 most common
   -r        relative freq per million
   -p        rank

Output
  - CSV file with columns:
         lemma,absolute-freq
  (-r)   lemma,rel-freq-per-million

Also generates a CSV file with the results named as <scriptname>_result.csv
"""
import spacy
from jjcli import *
from collections import Counter
import re
import os
import sys

pln = spacy.load("pt_core_news_lg")
voc = pln.vocab
freqsum = Counter()
freqabs = Counter()
freqrel = Counter()

def gprintcsv(fabs,frel,m=1000000, file=None):
    header = "word,occu,freq-per-mill,usual,rank,racio"
    if file:
        file.write(header + "\n")
    else:
        print(header)

    for pal,oco in fabs.most_common(m):
        freqhabitual = freqsum[pal]/freqabs[pal]*1000000
        racio = frel[pal] / freqhabitual
        r = voc[pal].rank
        if r > 1000000 :
            r = "OFV"
        line = f"{pal},{oco},{frel[pal]:.2f},{freqhabitual:.2f},{r},{racio:.2f}"
        if file:
            file.write(line + "\n")
        else:
            print(line)

def printcsv(f,m=1000000, file=None):
    header = "word,occu,freq-per-mill,rank,racio"
    if file:
        file.write(header + "\n")
    else:
        print(header)

    for pal,oco in f.most_common(m):
        freqhabitual = freqsum[pal]/freqabs[pal]*1000000
        racio = oco / freqhabitual
        r = voc[pal].rank
        if r > 1000000 :
            r = "OFV"
        line = f"{pal},{oco:.2f},{freqhabitual:.2f},{r},{racio:.2f}"
        if file:
            file.write(line + "\n")
        else:
            print(line)

def rank2freq(w,voc):
    r= min( voc[w].rank , voc[w.lower()].rank)
    if r > 1000000 :
        r = 1000000
    return 1 / (r + 2.7)  ## Zipf law variant

def main():
    cl = clfilter("pwlrm:", doc=__doc__ ) ### cl.opt
    
    num = int(cl.opt.get("-m",1000000))
    
    isrel = False
    if "-r" in cl.opt: 
        isrel = True

    # Nome do arquivo do script atual, sem extensão
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    outname = f"{script_name}_result.csv"

    freqabs.clear()
    freqsum.clear()
    freqrel.clear()

    for txt in cl.text():
        dt = pln(txt)
        for tok in dt:
            if tok.is_punct:
                continue
            if tok.is_stop:
                continue
            if tok.pos_ == "SPACE":
                continue

            lem = tok.lemma_

            if tok.pos_ != "PROPN":
                lem = re.sub(r" .*", r"", lem)
            else:
                lem = tok.text

            freqabs[lem] +=1 
            freqsum[lem] += rank2freq(tok.text, voc) 

    tot = freqabs.total()
    for pal,oco in freqabs.items():
        freqrel[pal] = oco / tot * 1000000

    with open(outname, "w", encoding="utf-8") as fout:
        if isrel:
            gprintcsv(freqabs, freqrel, num, file=fout)
        else:
            printcsv(freqabs, num, file=fout)

    if isrel:
        gprintcsv(freqabs, freqrel, num)
    else:
        printcsv(freqabs, num)


if __name__ == "__main__" : 
    main()