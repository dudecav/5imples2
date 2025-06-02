import csv
import nltk
import sys
from transformers import pipeline
from nltk.tokenize import sent_tokenize

def main():
    nltk.download("punkt")

    if len(sys.argv) < 2:
        print("Uso: python MakefileSentimento2.py <arquivo.txt>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            texto = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
        sys.exit(1)

    frases = sent_tokenize(texto)

    # Pipeline de análise de sentimentos
    nlp = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    output_file = input_file.replace(".txt", "_sentimentos.csv")

    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Frase", "Sentimento", "Confiança"])

        for frase in frases:
            resultado = nlp(frase)[0]
            writer.writerow([frase, resultado["label"], round(resultado["score"], 4)])

    print(f"\n✅ Análise concluída. Resultados salvos em: {output_file}")

if __name__ == "__main__":
    main()


