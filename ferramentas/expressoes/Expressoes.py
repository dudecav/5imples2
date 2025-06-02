"""
Usage:
  extrair_mwes.py texto1.txt [texto2.txt ...]

Output:
  - Gera extracao_mwes_result.csv
  - Lista as expressões mais frequentes de 2 e 3 palavras (MWEs)
"""

import spacy
import pandas as pd
from jjcli import *
from collections import Counter

pln = spacy.load("pt_core_news_lg")

def extrair_ngrams(doc, n=2):
    tokens = [t.text.lower() for t in doc if not t.is_punct and not t.is_space]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def main():
    cl = clfilter("", doc=__doc__)
    textos = cl.text()  # lista de textos carregados
    if not textos:
        print("⚠️ Por favor, indique ao menos um ficheiro .txt")
        return

    todos_bigrams = Counter()
    todos_trigrams = Counter()

    for texto in textos:
        doc = pln(texto)
        bigrams = extrair_ngrams(doc, 2)
        trigrams = extrair_ngrams(doc, 3)
        todos_bigrams.update(bigrams)
        todos_trigrams.update(trigrams)

    df_bi = pd.DataFrame(todos_bigrams.most_common(), columns=["expressao", "frequencia"])
    df_tri = pd.DataFrame(todos_trigrams.most_common(), columns=["expressao", "frequencia"])
    df_bi["tipo"] = "bigram"
    df_tri["tipo"] = "trigram"
    df = pd.concat([df_bi, df_tri], ignore_index=True)

    df.to_csv("extracao_mwes_result.csv", index=False, encoding="utf-8")
    print("✅ Resultado salvo em: extracao_mwes_result.csv")

if __name__ == "__main__":
    main()

