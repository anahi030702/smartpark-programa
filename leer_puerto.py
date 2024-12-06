#!/usr/bin/env python3
from datetime import datetime

from estacionamiento import Estacionamiento
from prueba import tomarFotoYEnviar
from sensor import Sensor

import serial
import time
import cv2
import requests
from bson import ObjectId


from conectToDb import ConectionDb


class puertoSerial:
    def __init__(self):
        self.port = 'COM6'
        self.baudrate = 9600
        self.timeout = 0
        self.est = Estacionamiento()
        self.est.leer_doc()
        self.db = ConectionDb()
        self.ser = serial.Serial(self.port, self.baudrate, timeout= self.timeout)


    def leer_puerto(self):
        # self.enviar_rfid_autorizados()  # Esta acción se ejecuta cada 5 minutos
        #
        # Espera un poco para que se establezca la conexión
        time.sleep(3)
        # # Variables para llevar el control de los tiempos
        # tiempo_ultimo_rfid = time.time()
        # tiempo_ultimo_accion = time.time()

        try:
            while True:
                # Verifica si han pasado 5 segundos (5000 milisegundos)
                # if time.time() - tiempo_ultimo_accion >= 3:
                if self.ser.in_waiting > 0:  # Verifica si hay datos disponibles para leer
                    line = self.ser.readline().decode('utf-8').rstrip()  # Lee la línea y decodifica
                    print(line)
                    fecha = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    parts = line.split(':')
                    if "UL" in parts[0]:
                        urlFoto = tomarFotoYEnviar()
                        sensor = Sensor(parts[0], urlFoto, fecha, parts[1])
                    else:
                        sensor = Sensor(parts[0], parts[1], fecha)
                    self.actualizarSensores(sensor)

                #     self.enviar_dato_alarma()
                #     self.mandarInfoLocal()
                #     self.actualizarEstacionamiento()
                #     # Espera 5 segundos antes de ejecutar nuevamente
                #     tiempo_ultimo_accion = time.time()
                #
                # # Verifica si han pasado 5 minutos (300 segundos)
                # if time.time() - tiempo_ultimo_rfid >= 300:
                #     self.enviar_rfid_autorizados()  # Esta acción se ejecuta cada 5 minutos
                #     tiempo_ultimo_rfid = time.time()



                #     # Espera 30 segundos antes de leer nuevamente
                time.sleep(5)

        except KeyboardInterrupt:
            print("Lectura interrumpida.")

        finally:
            self.ser.close()


    def enviar_dato_alarma(self):
        if self.db.conectar_mongo():
            res_final = ""
            res = self.db.findone( {"_id": ObjectId(self.est[0].noEs), "actuadores": {"$elemMatch": {"tipo": "AL-1"} } }, {"actuadores.$": 1})
            res1 = res["actuadores"]
            for res2 in res1:
                res_final = res2["valor"]
            if res_final == "0":
                dato = "AL-1:0"
                self.ser.write(dato.encode())  # Enviar como bytes
                time.sleep(0.1)
                print(dato)
                print("Enviado dato para apagar alarma")

    def enviar_rfid_autorizados(self):
        if self.db.conectar_mongo():
            rfid_autorizados = []
            res = self.db.findone( { "_id": ObjectId("673a970b8548904611656030") },{ "usuarios": 1, "_id": 0 })
            usus = res["usuarios"]
            for usu in usus:
                rfid_autorizados.append(usu["rfid"])
            data_to_send = ",".join(rfid_autorizados) + ","
            print(data_to_send)
            self.ser.write(data_to_send.encode())  # Enviar como bytes
            time.sleep(0.1)
            print("ENVIADOS LOS RFID AUTORIZADOS")

    def actualizarSensores(self, data):
        if self.db.conectar_mongo():
            if "AL" in data.tipo:
                print(data)
                res = self.db.updateone({"_id": ObjectId(self.est[0].noEs), "actuadores.tipo" : "AL-1"}, {"$set" : {"actuadores.$.valor": data.valor}})
                print(res)
                print("se mando el encendido de la alarma")
            elif "IN" in data.tipo:
                res = self.db.updateone({"_id": ObjectId(self.est[0].noEs), "sensores.tipo": data.tipo},
                                        {"$set": {"sensores.$.valor": data.valor}})
                print(res)
                print("cambio de estado de infrarojo")
            elif "UL" in data.tipo:
                data.tipo = "CA-1"
                res = self.db.updateone({"_id": ObjectId(self.est[0].noEs)}, {"$push" : {"actuadores": data.dict()}})
                print(res)
                print("se guardo la imagen de exeso de velocidad")
            else:
                res = self.db.updateone({"_id": ObjectId(self.est[0].noEs)}, {"$push" : {"sensores": data.dict()}})
                print(res)
                # if not res:
                #     self.est[0].sensores.agregar(data)
                #     self.est.document(self.est.dict())
                #     print("Valor guardado localmente hasta que se cree el estacionamiento en la BD")
        else:
            self.est[0].sensores.agregar(data)
            self.est.document(self.est.dict())
            print("Valor guardado localmente")

    def mandarInfoLocal(self):
        if self.db.conectar_mongo() is None:
            print("sigue sin haber conexion con la BD")
        elif not self.est[0].sensores:
            print("no hay informacion de sensores para subir")
        elif self.est[0].noEs == "":
            print("El estacionamiento aun no existe en la BD")
        else:
            for sensor in self.est[0].sensores:
                if sensor.tipo == "AL-1":
                    res = self.db.updateone({"_id": ObjectId(self.est[0].noEs), "actuadores.tipo": "AL-1"},{"$set": {"actuadores.$.valor": sensor.valor}})
                    print(res)
                elif "IN" in sensor.tipo:
                    res = self.db.updateone({"_id": ObjectId(self.est[0].noEs), "sensores.tipo": sensor.tipo},
                                            {"$set": {"sensores.$.valor": sensor.valor}})
                    print(res)
                else:
                    res = self.db.updateone({"_id": ObjectId(self.est[0].noEs)}, {"$push" : {"sensores": sensor.dict()}})
                    print(res)
            self.est[0].sensores = Sensor()
            self.est.document(self.est.dict())


    def actualizarEstacionamiento(self):
        dicLocal = self.est[0].dict()
        if self.db.conectar_mongo():
            if self.est[0].noEs == "":
                id = self.db.create(self.est.dict(), 1)
                self.est[0].noEs = str(id)
                self.est.document(self.est.dict())
            else:
                res = self.db.findone({"_id": ObjectId("673a970b8548904611656030")})
                if res["nombre"] == dicLocal["nombre"] and res["ubicacion"] == dicLocal["ubicacion"]:
                    print("No hay cambios que mandar a mongo")
                else:
                    self.db.updateone({"_id": ObjectId(self.est[0].noEs)}, {"$set": {"nombre": dicLocal["nombre"], "ubicacion": dicLocal["ubicacion"]}})
                    print("hay cambios que mandar a mongo")
        else:
            print("La informacion se mantendra en local hasta que se restablezca la conexion con la BD")

    def tomarFotoYEnviar():
        # Cambia el índice de la cámara según sea necesario (1 para cámara externa)
        cap = cv2.VideoCapture(1)

        # Verifica si la cámara se ha abierto correctamente
        if not cap.isOpened():
            print("No se pudo acceder a la cámara.")
            exit()

        # Captura un solo frame
        ret, frame = cap.read()

        if ret:
            # Guarda temporalmente la imagen en disco
            filename = "foto_a_enviar.jpg"
            cv2.imwrite(filename, frame)  # Guarda la imagen

            # Endpoint de Laravel al que enviarás la imagen
            url = "http://3.147.187.80/api/estacion/673a970b8548904611656030/actuadores/camara/guardar"

            # Prepara los datos para enviar
            with open(filename, 'rb') as file:
                files = {'imagen': file}  # Cambia 'imagen' por el nombre esperado en el request del backend
                response = requests.post(url, files=files)

            # Muestra la respuesta del servidor
            if response.status_code == 200:
                print("Imagen enviada correctamente:", response.json())
                return response.json()["path"]
            else:
                print("Error al enviar la imagen:", response.status_code, response.text)
        else:
            print("No se pudo capturar la foto.")

        # Libera la cámara
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    puertoSerial().leer_puerto()
