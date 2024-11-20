import numpy as np
import csv
from scipy import stats
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox
import requests
from Dado import Dado
from Funcoes_de_arquivo import escrever_no_aquivo

# chave api OpenWeather
API_KEY = "94daa8d6048635a335d1c8ee1ff346f2"



def criar_arquivo_csv():
    def salvar_arquivo():
        try:
            dados = entrada_dados.get("1.0", END).strip()
            linhas = [linha.strip() for linha in dados.split("\n") if linha.strip()]
            temperaturas = [float(linha) for linha in linhas]  # Garante que só números sejam inseridos
            caminho_arquivo = filedialog.asksaveasfilename(
                title="Salvar Arquivo CSV",
                defaultextension=".csv",
                filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*"))
            )
            if caminho_arquivo:
                with open(caminho_arquivo, mode='w', newline='') as file:
                    escritor = csv.writer(file)
                    for temperatura in temperaturas:
                        escritor.writerow([temperatura])
                messagebox.showinfo("Sucesso", "Arquivo CSV criado com sucesso!")
                janela_criacao.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números válidos, um por linha.")

    janela_criacao = Toplevel()
    janela_criacao.title("Criar Novo Arquivo CSV")
    janela_criacao.geometry("400x300")

    Label(janela_criacao, text="Insira as temperaturas (um valor por linha):", font=("Arial", 12)).pack(pady=10)
    entrada_dados = Text(janela_criacao, width=40, height=10, font=("Arial", 12))
    entrada_dados.pack(pady=10)

    btn_salvar = Button(janela_criacao, text="Salvar", command=salvar_arquivo)
    btn_salvar.pack(pady=10)


def editar_arquivo_csv():
    def carregar_arquivo_para_edicao():
        nonlocal caminho_arquivo
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo CSV",
            filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*"))
        )
        if caminho_arquivo:
            try:
                with open(caminho_arquivo, mode='r') as file:
                    leitor = csv.reader(file)
                    dados = "\n".join([row[0] for row in leitor if row])
                entrada_dados.delete("1.0", END)
                entrada_dados.insert("1.0", dados)
            except FileNotFoundError:
                messagebox.showerror("Erro", "Arquivo não encontrado.")
            except Exception:
                messagebox.showerror("Erro", "Erro ao carregar o arquivo.")

    def salvar_edicoes():
        try:
            dados = entrada_dados.get("1.0", END).strip()
            linhas = [linha.strip() for linha in dados.split("\n") if linha.strip()]
            temperaturas = [float(linha) for linha in linhas]  # Valida os dados como números
            with open(caminho_arquivo, mode='w', newline='') as file:
                escritor = csv.writer(file)
                for temperatura in temperaturas:
                    escritor.writerow([temperatura])
            messagebox.showinfo("Sucesso", "Arquivo CSV editado com sucesso!")
            janela_edicao.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números válidos, um por linha.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {str(e)}")

    caminho_arquivo = None

    janela_edicao = Toplevel()
    janela_edicao.title("Editar Arquivo CSV")
    janela_edicao.geometry("400x300")

    btn_carregar = Button(janela_edicao, text="Carregar Arquivo CSV", command=carregar_arquivo_para_edicao)
    btn_carregar.pack(pady=10)

    entrada_dados = Text(janela_edicao, width=40, height=10, font=("Arial", 12))
    entrada_dados.pack(pady=10)

    btn_salvar = Button(janela_edicao, text="Salvar Edições", command=salvar_edicoes)
    btn_salvar.pack(pady=10)


#serve para criar uma arquivo csv novo
def criar_arquivo_csv():
    caminho_arquivo = filedialog.asksaveasfilename(
        title="Salvar Arquivo CSV",
        defaultextension=".csv",
        filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*"))
    )
    if caminho_arquivo:
        # Cria um arquivo vazio sem cabeçalhos
        with open(caminho_arquivo, mode='w') as file:
            pass  # Apenas cria o arquivo sem escrever nada
        messagebox.showinfo("Sucesso", "Arquivo CSV vazio criado com sucesso!")
        return caminho_arquivo
    return None

# carregamento de arquivo csv
def carregar_dados_csv(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r') as file:
            leitor = csv.reader(file)
            temperaturas = [float(row[0]) for row in leitor if row]
        return np.array(temperaturas)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo não encontrado. Verifique o caminho do arquivo e tente novamente.")
        return None
    except ValueError:
        messagebox.showerror("Erro", "Erro ao processar os dados. O arquivo deve conter apenas números válidos.")
        return None

# calcular stats
def calcular_estatisticas(temperaturas):
    media = np.mean(temperaturas)
    mediana = np.median(temperaturas)
    moda = stats.mode(temperaturas, keepdims=True).mode[0]
    desvio_padrao = np.std(temperaturas)
    variancia = np.var(temperaturas)

    return {
        'media': media,
        'mediana': mediana,
        'moda': moda,
        'desvio_padrao': desvio_padrao,
        'variancia': variancia
    }

# grafico
def criar_grafico(temperaturas):
    datas = [f"Dia {i+1}" for i in range(len(temperaturas))]
    media = np.mean(temperaturas)
    mediana = np.median(temperaturas)
    moda = stats.mode(temperaturas, keepdims=True).mode[0]

    plt.figure(figsize=(12, 6))
    plt.bar(datas, temperaturas, color='red', edgecolor='black')

    for i, temp in enumerate(temperaturas):
        plt.text(i, temp + 1, f"{temp}°C", ha='center', fontsize=10)

    plt.text(len(datas) - 2, max(temperaturas) + 2,
             f"Média: {media:.1f}°C\nModa: {moda}°C\nMediana: {mediana:.1f}°C",
             fontsize=12, color="black")

    plt.ylim(0, max(temperaturas) + 10)
    plt.ylabel("°C", fontsize=12)
    plt.xlabel("Dias", fontsize=12)
    plt.title("Temperaturas Registradas", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    plt.show()

# previsao do tempo api openweather
def obter_previsao_tempo(cidade):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&units=metric&lang=pt_br&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        temp_atual = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        return f"Previsão do tempo em {cidade.capitalize()}:\n{descricao.capitalize()}, {temp_atual}°C"
    except requests.exceptions.HTTPError as http_err:
        return f"Erro HTTP: {http_err.response.status_code}. Verifique o nome da cidade."
    except requests.exceptions.RequestException:
        return "Erro ao conectar à API. Verifique sua conexão com a internet."


def selecionar_arquivo():
    global temperaturas
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo CSV",
        filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*"))
    )
    if caminho_arquivo:
        temperaturas = carregar_dados_csv(caminho_arquivo)
        if temperaturas is not None:
            estatisticas = calcular_estatisticas(temperaturas)
            exibir_estatisticas(estatisticas)
            criar_grafico(dados, temperaturas)
            btn_grafico["state"] = NORMAL
        else:
            temperaturas = None
            btn_grafico["state"] = DISABLED

# exibir stats
def exibir_estatisticas(estatisticas):
    estatisticas_texto.set(
        f"Média: {estatisticas['media']:.2f}\n"
        f"Mediana: {estatisticas['mediana']:.2f}\n"
        f"Moda: {estatisticas['moda']:.2f}\n"
        f"Desvio Padrão: {estatisticas['desvio_padrao']:.2f}\n"
        f"Variância: {estatisticas['variancia']:.2f}"
    )

# previsao do tempo
def mostrar_previsao():
    cidade = entrada_cidade.get()
    if cidade:
        previsao = obter_previsao_tempo(cidade)
        previsao_texto.set(previsao)
    else:
        messagebox.showwarning("Aviso", "Por favor, insira o nome de uma cidade.")

# interface
def criar_interface():
    global estatisticas_texto, btn_grafico, previsao_texto, entrada_cidade, temperaturas

    janela = Tk()
    janela.title("Análise de Temperaturas")
    janela.geometry("400x500")

    # Botão para criar novo arquivo CSV
    btn_criar = Button(janela, text="Criar Novo Arquivo CSV", command=criar_arquivo_csv)
    btn_criar.pack(pady=10)

    # Botão para editar arquivo CSV existente
    btn_editar = Button(janela, text="Editar Arquivo CSV", command=editar_arquivo_csv)
    btn_editar.pack(pady=10)

    # Botão para selecionar arquivo CSV
    btn_selecionar = Button(janela, text="Selecionar Arquivo CSV", command=selecionar_arquivo)
    btn_selecionar.pack(pady=10)

    # Label para estatísticas
    estatisticas_texto = StringVar()
    lbl_estatisticas = Label(janela, textvariable=estatisticas_texto, justify=LEFT, font=("Arial", 12))
    lbl_estatisticas.pack(pady=10)

    # botao graficos
    btn_grafico = Button(janela, text="Exibir Gráfico", command=lambda: criar_grafico(dados, temperaturas), state=DISABLED)
    btn_grafico.pack(pady=10)

    # Previsão do tempo
    frame_previsao = Frame(janela)
    frame_previsao.pack(pady=20)

    Label(frame_previsao, text="Cidade:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
    entrada_cidade = Entry(frame_previsao, width=20, font=("Arial", 12))
    entrada_cidade.grid(row=0, column=1, padx=5)

    btn_previsao = Button(frame_previsao, text="Ver Previsão", command=mostrar_previsao)
    btn_previsao.grid(row=0, column=2, padx=5)

    previsao_texto = StringVar()
    lbl_previsao = Label(janela, textvariable=previsao_texto, justify=LEFT, font=("Arial", 12), wraplength=350)
    lbl_previsao.pack(pady=10)

    janela.mainloop()


if __name__ == "__main__":
    criar_interface()
