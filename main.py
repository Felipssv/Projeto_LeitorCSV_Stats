import numpy as np
import csv
from scipy import stats


def carregar_dados_csv(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r') as file:
            leitor = csv.reader(file)
            # temperaturas na primeira coluna
            temperaturas = [float(row[0]) for row in leitor if row]
        return np.array(temperaturas)
    except FileNotFoundError:
        print("Arquivo não encontrado. Verifique o caminho do arquivo e tente novamente.")
        return None
    except ValueError:
        print("Erro ao processar os dados. Verifique se o arquivo contém apenas números válidos.")
        return None


# estatisticas calculadas
def calcular_estatisticas(temperaturas):
    media = np.mean(temperaturas)
    mediana = np.median(temperaturas)
    moda = stats.mode(temperaturas)[0]  # [0][0] para extrair o valor da moda
    desvio_padrao = np.std(temperaturas)
    variancia = np.var(temperaturas)

    return {
        'media': media,
        'mediana': mediana,
        'moda': moda,
        'desvio_padrao': desvio_padrao,
        'variancia': variancia
    }


def main():

    caminho_arquivo = input("Por favor, insira o caminho completo do arquivo CSV: ")

    temperaturas = carregar_dados_csv(caminho_arquivo)

    if temperaturas is not None:
        estatisticas = calcular_estatisticas(temperaturas)

        print(f"Média: {estatisticas['media']:.2f}")
        print(f"Mediana: {estatisticas['mediana']:.2f}")
        print(f"Moda: {estatisticas['moda']:.2f}")
        print(f"Desvio Padrão: {estatisticas['desvio_padrao']:.2f}")
        print(f"Variância: {estatisticas['variancia']:.2f}")
    else:
        print("Não foi possível calcular as estatísticas devido a um erro ao carregar os dados.")


if __name__ == "__main__":
    main()
