import numpy as np
import csv
from scipy import stats
import matplotlib.pyplot as plt


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


def criar_grafico(temperaturas):
    # Gerar datas automaticamente para o gráfico
    datas = [f"Dia {i+1}" for i in range(len(temperaturas))]

    # Cálculo das estatísticas
    media = np.mean(temperaturas)
    mediana = np.median(temperaturas)

    # Tratar o retorno da moda adequadamente
    moda_resultado = stats.mode(temperaturas, keepdims=True)  # Garantir que o retorno seja um array
    moda = moda_resultado.mode[0]  # Extrair o valor da moda

    # Criação do gráfico
    plt.figure(figsize=(12, 6))
    plt.bar(datas, temperaturas, color='red', edgecolor='black')

    # Adicionar os valores no topo das barras
    for i, temp in enumerate(temperaturas):
        plt.text(i, temp + 1, f"{temp}°C", ha='center', fontsize=10)

    # Adicionar as estatísticas no gráfico
    plt.text(len(datas) - 2, max(temperaturas) + 2,
             f"Média: {media:.1f}°C\nModa: {moda}°C\nMediana: {mediana:.1f}°C",
             fontsize=12, color="black")

    # Configurações do gráfico
    plt.ylim(0, max(temperaturas) + 10)
    plt.ylabel("°C", fontsize=12)
    plt.xlabel("Dias", fontsize=12)
    plt.title("Temperaturas Registradas", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Exibir o gráfico
    plt.show()



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

        criar_grafico(temperaturas)
    else:
        print("Não foi possível calcular as estatísticas devido a um erro ao carregar os dados.")


if __name__ == "__main__":
    main()
