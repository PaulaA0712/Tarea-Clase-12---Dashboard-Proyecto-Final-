# paquetes.py

from clasificador import Clasificador
from datos import COSTOS_BASE

class Paquete:

    def __init__(self, peso, destino):
        self.peso = peso
        self.destino = destino
        self.tipo = Clasificador.clasificar(peso)

    def calcular_costo(self):
        if self.tipo == "Documento":
            return COSTOS_BASE["Documento"]
        elif self.tipo == "Paquetería":
            return COSTOS_BASE["Paquetería"] + self.peso * 1000
        else:
            return COSTOS_BASE["Carga"] + self.peso * 2000