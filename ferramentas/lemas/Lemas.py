"""
Usage:
 extratorlemas.py [Options] files
 Options:
   -m 10     mostra só os 10 lemas mais comuns

Output:
  - CSV com: lema, frequência
  - Nome do ficheiro de saída: <nome_do_script>_result.csv
"""

import spacy
from jjcli import *
from collections import Counter
import os
import sys

pln = spacy.load("pt_core_news_lg")

def main():
    cl = clfilter("m:", doc=__doc__)
    num = int(cl.opt.get("-m", 1000000))

    lemas = Counter()

    for txt in cl.text():
        doc = pln(txt)
        for tok in doc:
            if tok.is_punct or tok.is_space or tok.is_stop:
                continue
            lemas[tok.lemma_] += 1

    # Salva em CSV
    scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    outname = f"{scriptname}_result.csv"
    with open(outname, "w", encoding="utf-8") as fout:
        fout.write("lema,frequencia\n")
        for lema, freq in lemas.most_common(num):
            fout.write(f"{lema},{freq}\n")

    print(f"✅ Resultado salvo em: {outname}")

if __name__ == "__main__":
    main()
