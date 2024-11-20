import os
import csv
from Dado import Dado
from tkinter import filedialog, messagebox, Toplevel
from tkinter import *



class DataInvalidaException(Exception):
    pass

class HorarioInvalidoException(Exception):
    pass

def criar_arquivo(nome):
    arquivo = open(f"{nome}.csv", "w")
    arquivo.close()

def verificar_dados(dado):
    #As if statements até a linha 33 servem para ver se a data está formatada corretamente
    if int(dado.mes) < 0 or int(dado.mes) > 12:
        raise DataInvalidaException("MÊS INVÁLIDO! (Deve estar entre 1 e 12)")
    elif int(dado.dia) < 1:
        raise DataInvalidaException("DIA INVÁLIDO! (Não pode ser menor que 1)")
    
    if int(dado.mes) == 2:
        if int(dado.dia) > 29:
            raise DataInvalidaException(f"DIA INVÁLIDO! (O mês {dado.mes} não tem o dia {dado.dia})")
        elif not dado.bissexto and int(dado.dia) == 29:
            raise DataInvalidaException(f"DIA INVÁLIDO! (O ano {dado.ano} não é bissexto, portanto o mês de fevereiro não tem o dia 29)")
        
    if (int(dado.mes) <= 6 and int(dado.mes) % 2 == 0) or (int(dado.mes)>= 7 and int(dado.mes) % 2 != 0):
        if int(dado.dia) == 31:
            raise DataInvalidaException(f"DIA INVÁLIDO! (O mês {dado.mes} não tem o dia {dado.dia})")

    #Essa if statement serve para verificar se o horário está formatado corretamente
    if len(dado.string_horas) > 2 or len(dado.string_minutos) > 2:
        raise HorarioInvalidoException("HORÁRIO INVÁLIDO! (Os campos de hora e minutos só podem ter até dois caracteres!)")
    elif (dado.horas < 0) or (int(dado.minutos) < 0):
        raise HorarioInvalidoException("HORÁRIO INVÁLIDO! (Não coloque números negativos!)")
    elif int(dado.horas) > 23:
        raise HorarioInvalidoException("HORÁRIO INVÁLIDO! (Esse campo não pode ter um número maior que 23!)")
    elif int(dado.minutos) > 59:
        raise HorarioInvalidoException("HORÁRIO INVÁLIDO! (Esse campo não pode ter um número maior que 59!)")
            
def escrever_no_aquivo(): 
    nome_do_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo",
        filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")))
    if nome_do_arquivo:
        try:
            #Cria a janela
            janela_adcionar = Toplevel()
            janela_adcionar.title("Adcionar dados ao CSV")
            janela_adcionar.geometry("300x300")

            Label(janela_adcionar, text="Adicionar Dados", font=("Arial", 12, "bold")).pack(pady=10)

            frame_inputs = Frame(janela_adcionar)
            frame_inputs.pack(pady=10)

            # Campos de entrada
            Label(frame_inputs, text="Temperatura (°C):").grid(row=0, column=0, padx=5, pady=5)
            entrada_temperatura = Entry(frame_inputs)
            entrada_temperatura.grid(row=0, column=1, padx=5, pady=5)

            Label(frame_inputs, text="Dia:").grid(row=1, column=0, padx=5, pady=5)
            entrada_dia = Entry(frame_inputs)
            entrada_dia.grid(row=1, column=1, padx=5, pady=5)

            Label(frame_inputs, text="Mês:").grid(row=2, column=0, padx=5, pady=5)
            entrada_mes = Entry(frame_inputs)
            entrada_mes.grid(row=2, column=1, padx=5, pady=5)

            Label(frame_inputs, text="Ano:").grid(row=3, column=0, padx=5, pady=5)
            entrada_ano = Entry(frame_inputs)
            entrada_ano.grid(row=3, column=1, padx=5, pady=5)

            Label(frame_inputs, text="Horas:").grid(row=4, column=0, padx=5, pady=5)
            entrada_horas = Entry(frame_inputs)
            entrada_horas.grid(row=4, column=1, padx=5, pady=5)

            Label(frame_inputs, text="Minutos:").grid(row=5, column=0, padx=5, pady=5)
            entrada_minutos = Entry(frame_inputs)
            entrada_minutos.grid(row=5, column=1, padx=5, pady=5)

            def salvar_dados():
                try:
                    temperatura = float(entrada_temperatura.get())
                    dia = int(entrada_dia.get())
                    mes = int(entrada_mes.get())
                    ano = int(entrada_ano.get())
                    horas = str(entrada_horas.get())
                    minutos = str(entrada_minutos.get())
                    
                    dado = Dado(temperatura,dia,mes,ano,horas,minutos)
                    verificar_dados(dado)
                    with open(nome_do_arquivo, mode = "a", newline = '') as arquivo_csv:
                        escritor = csv.writer(arquivo_csv, delimiter=',')
                        escritor.writerow([dado.temperatura, 
                                            dado.dia, 
                                            dado.mes, 
                                            dado.ano, 
                                            dado.horas, 
                                            dado.minutos,
                                            dado.string_horas,
                                            dado.string_minutos])
                    messagebox.showinfo("Sucesso!","Dados salvos com sucesso!")
                    janela_adcionar.destroy()
                except FileNotFoundError:
                    messagebox.showerror("Erro", "Arquivo não encontrado")
                except HorarioInvalidoException:
                    messagebox.showerror("Erro", "Horário inválido!")
                except DataInvalidaException:
                    messagebox.showerror("Erro", "Data inválida!")
            btn_salvar = Button(janela_adcionar, text="Salvar dados", command=salvar_dados)
            btn_salvar.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo não encontrado")