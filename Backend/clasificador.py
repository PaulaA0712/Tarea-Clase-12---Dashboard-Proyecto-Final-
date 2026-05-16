# clasificador.py

class Clasificador:

    @staticmethod
    def clasificar(peso):
        if peso < 1:
            return "Documento"
        elif peso <= 10:
            return "Paquetería"
        else:
            return "Carga"