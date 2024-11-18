from functools import total_ordering
from typing import Self

@total_ordering
class Dado:
    bissexto = False
    horas = None
    minutos = None

    #OBSERVAÇÃO: "horas" e "minutos" devem ser strings!
    def __init__(self, temperatura, dia, mes, ano, horas, minutos):
        self.temperatura = temperatura
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.string_horario = f"{horas}:{minutos}"
        if horas[0] == "0":
            self.horas = int(horas[1])
        else:
            self.horas = int(horas)

        if minutos[0] == "0":
            self.minutos = int(minutos[1])
        else:
            self.minutos = int(minutos)

        if (ano % 4 == 0 and ano % 100 != 0) or (ano % 100 == 0 and ano % 400 == 0):
            self.bissexto = True
        else:
            self.bissexto = False

    def __lt__(self, other: Self):
        return ((self.ano, self.mes, self.dia, self.horas, self.minutos) <
                (other.ano, other.mes, other.dia, other.horas, other.minutos))
