from transformers import pipeline
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python analise_sentimentos.py arquivo.txt")
        return

    arquivo = sys.argv[1]

    # Criar pipeline de análise de sentimento multilíngue
    nlp = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    with open(arquivo, "r", encoding="utf-8") as f:
        texto = f.read()

    # Pode dividir o texto em frases para análise mais detalhada
    frases = texto.split(".")  # simples split por ponto final

    resultados = []
    for frase in frases:
        frase = frase.strip()
        if frase:
            resultado = nlp(frase)[0]
            resultados.append((frase, resultado['label']))

    # Salvar resultados em arquivo
    arquivo_saida = "resultado_sentimentos.txt"
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for frase, sentimento in resultados:
            f.write(f"{sentimento}: {frase}\n")

    print(f"Análise de sentimentos concluída. Resultado salvo em {arquivo_saida}.")

if __name__ == "__main__":
    main()
