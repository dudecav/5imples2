"""
Usage:
 grafopersonagens.py [Options] files
 Options:
   -w 5     tamanho da janela de contexto (padrão: 5 frases)

Output:
  - Grafo de conexões entre personagens (tipo PER)
  - Salvo em: grafopersonagens_result.graphml
"""

import spacy
from jjcli import *
from collections import defaultdict
import networkx as nx
import os
import sys

pln = spacy.load("pt_core_news_lg")

def extrair_personagens(doc):
    """Retorna uma lista de nomes de pessoas no documento."""
    return [ent.text for ent in doc.ents if ent.label_ == "PER"]

def main():
    cl = clfilter("w:", doc=__doc__)
    janela = int(cl.opt.get("-w", 5))  # número de frases por janela

    G = nx.Graph()

    for txt in cl.text():
        doc = pln(txt)
        frases = list(doc.sents)

        for i in range(0, len(frases), janela):
            bloco = frases[i:i+janela]
            texto_bloco = " ".join([sent.text for sent in bloco])
            subdoc = pln(texto_bloco)
            pessoas = list(set(extrair_personagens(subdoc)))

            for i in range(len(pessoas)):
                for j in range(i + 1, len(pessoas)):
                    a, b = pessoas[i], pessoas[j]
                    if G.has_edge(a, b):
                        G[a][b]["weight"] += 1
                    else:
                        G.add_edge(a, b, weight=1)

    # Salvar o grafo
    outname = "grafopersonagens_result.graphml"
    nx.write_graphml(G, outname)
    print(f"✅ Grafo salvo em: {outname}")

if __name__ == "__main__":
    main()