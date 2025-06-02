"""
Usage:
  MakefileEstilosLing.py texto1.txt texto2.txt [texto3.txt ...]

Output:
  - Gera: comparar_estilo_result.csv
  - Compara estilo de linguagem de 2 ou mais textos
"""

import spacy
import pandas as pd
import sys
from collections import Counter

# Carrega o modelo do spaCy para português
pln = spacy.load("pt_core_news_lg")

def analisar_texto(texto):
    doc = pln(texto)
    tokens = [t for t in doc if not t.is_space and not t.is_punct]
    
    total_tokens = len(tokens)
    total_frases = len(list(doc.sents))
    comprimento_medio_frase = total_tokens / total_frases if total_frases > 0 else 0
    tipos_palavras = len(set(t.lemma_ for t in tokens))
    
    pos_counter = Counter(t.pos_ for t in tokens)
    pronouns = sum(1 for t in tokens if t.pos_ == "PRON")
    advs = pos_counter.get("ADV", 0)
    
    return {
        "total_palavras": total_tokens,
        "tipos_diferentes": tipos_palavras,
        "frases": total_frases,
        "comprimento_medio_frase": round(comprimento_medio_frase, 2),
        "pronomes": pronouns,
        "advérbios": advs,
        "verbos": pos_counter.get("VERB", 0),
        "substantivos": pos_counter.get("NOUN", 0),
        "adjetivos": pos_counter.get("ADJ", 0)
    }

def main():
    arquivos = sys.argv[1:]
    if len(arquivos) < 2:
        print("⚠️ Por favor, indique pelo menos dois ficheiros .txt para comparação.")
        return

    resultados = {}

    for nome in arquivos:
        try:
            with open(nome, encoding="utf-8") as f:
                texto = f.read()
            resultados[nome] = analisar_texto(texto)
        except Exception as e:
            print(f"Erro ao processar {nome}: {e}")

    df = pd.DataFrame.from_dict(resultados, orient="index")
    df.to_csv("comparar_estilo_result.csv", encoding="utf-8")
    print("✅ Comparação concluída. Resultado salvo em: comparar_estilo_result.csv")

if __name__ == "__main__":
    main()

