#!/usr/bin/env python3
from datetime import datetime

from estacionamiento import Estacionamiento
from sensor import Sensor

import serial
import time
import json
from bson import ObjectId


from conectToDb import ConectionDb


class puertoSerial:
    def __init__(self):
        self.port = 'COM3'
        self.baudrate = 9600
        self.timeout = 0
        self.est = Estacionamiento()
        self.est.leer_doc()
        self.db = ConectionDb()

    def leer_puerto(self):
        # Inicializa la conexión serial
        ser = serial.Serial(self.port, self.baudrate, timeout= self.timeout)

        # Espera un poco para que se establezca la conexión
        time.sleep(2)

        try:
            while True:
                if ser.in_waiting > 0:  # Verifica si hay datos disponibles para leer
                    line = ser.readline().decode('utf-8').rstrip()  # Lee la línea y decodifica
                    fecha = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    parts = line.split(':')
                    sensor = Sensor(parts[0], parts[1], fecha)
                    self.mandarInfoLocal()
                    self.actualizarSensores(sensor)




        except KeyboardInterrupt:
            print("Lectura interrumpida.")

        finally:
            ser.close()


    def actualizarSensores(self, data):
        if self.db.conectar_mongo():
            res = self.db.updateone({"_id": ObjectId(self.est[0].noEs)}, {"$push" : {"sensores": data.dict()}})
            print(res)
        else:
            self.est[0].sensores.agregar(data)
            self.est.document(self.est.dict())
            print("Valor guardado localmente")

    def mandarInfoLocal(self):
        if self.db.conectar_mongo() and self.est[0].sensores:
            for sensor in self.est[0].sensores:
                print(sensor.dict())
                res = self.db.updateone({"_id": ObjectId(self.est[0].noEs)}, {"$push" : {"sensores": sensor.dict()}})
                print(res)

            self.est[0].sensores = Sensor()
            self.est.document(self.est.dict())
        else:
            print("no hay informacion de sensores para subir")




if __name__ == "__main__":
    puertoSerial().leer_puerto()
