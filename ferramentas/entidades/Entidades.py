"""
Usage:
 entidadesnomeadas.py [Options] files
 Options:
   -m 10     mostra só as 10 entidades mais comuns

Output:
  - CSV com: entidade, tipo, frequência
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

    entidades = Counter()
    tipos = {}

    for txt in cl.text():
        doc = pln(txt)
        for ent in doc.ents:
            entidades[ent.text] += 1
            tipos[ent.text] = ent.label_

    # Salva em CSV
    scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    outname = f"{scriptname}_result.csv"
    with open(outname, "w", encoding="utf-8") as fout:
        fout.write("entidade,tipo,frequencia\n")
        for ent, freq in entidades.most_common(num):
            fout.write(f"{ent},{tipos[ent]},{freq}\n")

    print(f"✅ Resultado salvo em: {outname}")

if __name__ == "__main__":
    main()
