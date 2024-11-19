import os
import csv
from Dado import Dado



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
    if len(dado.horas) > 2 or len(dado.minutos) > 2:
        raise HorarioInvalidoException("HORÁRIO INVÁLIDO! (Os campos de hora e minutos só podem ter até dois caracteres!)")
    elif (int(dado.horas) < 0) or (int(dado.horas[1]) < 0) or (int(dado.minutos) < 0) or (int(dado.minutos[1]) < 0):
        raise HorarioInvalidoException("HORÁRIO INVÁLIDO! (Não coloque números negativos!)")
    elif int(dado.horas) > 23:
        raise HorarioInvalidoException("HORÁRIO INVÁLIDO! (Esse campo não pode ter um número maior que 23!)")
    elif int(dado.minutos) > 59:
        raise HorarioInvalidoException("HORÁRIO INVÁLIDO! (Esse campo não pode ter um número maior que 59!)")
            
def escrever_no_aquivo(nome_do_arquivo, dado):
    if not os.path.exists(f"{nome_do_arquivo}.csv"):
        raise FileNotFoundError()
    with open(f'{nome_do_arquivo}.csv', mode = "a", newline = '') as arquivo_csv:
        escritor = csv.writer(arquivo_csv, delimiter=',')
        escritor.writerow([dado.temperatura, 
                           dado.dia, 
                           dado.mes, 
                           dado.ano, 
                           dado.horas, 
                           dado.minutos,
                           dado.string_horas,
                           dado.string_minutos])
