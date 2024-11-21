from math import remainder
from functools import total_ordering
from typing import Self


@total_ordering
class Dado:
    bissexto = False
    horas = None
    minutos = None

    # OBSERVAÇÃO: "horas" e "minutos" devem ser strings!
    def __init__(self, temperatura, dia, mes, ano, horas, minutos):
        self.temperatura = temperatura
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.string_horas = horas
        self.string_minutos = minutos
        if horas[0] == "0":
            self.horas = int(horas[1])
        else:
            self.horas = int(horas)

        if minutos[0] == "0":
            self.minutos = int(minutos[1])
        else:
            self.minutos = int(minutos)

        if (remainder(int(ano), 4) == 0 and remainder(int(ano), 100) != 0) or (
                remainder(int(ano), 100) == 0 and remainder(int(ano), 400) == 0):
            self.bissexto = True
        else:
            self.bissexto = False

    def __lt__(self, other: Self):
        return ((self.ano, self.mes, self.dia, self.horas, self.minutos) <
                (other.ano, other.mes, other.dia, other.horas, other.minutos))
