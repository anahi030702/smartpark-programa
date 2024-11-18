import json
import os

class Arreglo:
    def __init__(self):
        self.arreglos = []

    def __str__(self):
        return '\n'.join(str(arreglo) for arreglo in self.arreglos)
        # return json.dumps(self.arreglos, indent=4)

    # Métodos para cuando funciona como arreglo
    # regresa el valor que se encuentra en el indices especificado
    def __getitem__(self, index):
        return self.arreglos[index]

    # edita el valor del indice que se especifique
    def __setitem__(self, index, valor):
        self.arreglos[index] = valor

    # regresa el numero de elementos que tiene el array
    def __len__(self):
        return len(self.arreglos)

    # Elimina el elmento del indice que le indiquemos
    def __delitem__(self, index):
        del self.arreglos[index]

    # agrega al array el elemento que se le pasa
    def agregar(self, valor):
        self.arreglos.append(valor)

    def buscar_indice(self, valor):
        try:
            return self.arreglos.index(valor)
        except ValueError:
            return -1  # Devuelve -1 si el valor no se encuentra

    def vaciar(self):
        self.arreglos.clear()

