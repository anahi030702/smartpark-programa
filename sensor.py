import json

from arreglo import Arreglo


class Sensor(Arreglo):
    def __init__(self, tipo=None, valor= None, fecha = None, velocidad=None):
        if tipo is not None:
            self.tipo = tipo
            self.valor = valor
            self.fecha = fecha
            self.velocidad = velocidad
            self._is_array = False
        else:
            self._is_array = True
            super().__init__()

    def __str__(self):
        if self._is_array:
            return super().__str__()
        else:
            velocidad_info = f", velocidad={self.velocidad}" if self.velocidad is not None else ""
            return f"Sensor(tipo={self.tipo}, valor={self.valor}, fecha={self.fecha}{velocidad_info})"


    def dict(self):
        if self._is_array:
            return [arreglo.dict() for arreglo in self.arreglos]
        else:
            data = {"tipo": self.tipo, "valor": self.valor, "fecha": self.fecha}
            if self.velocidad is not None:
                data["velocidad"] = self.velocidad
            return data

    def iterar_archivo(self, data):
        sensores = []

        for doc in data:
            sensor = Sensor(doc["tipo"], doc["valor"], doc["fecha"])
            sensores.append(sensor)
        self.arreglos = sensores
        return sensores

