import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class ConectionDb:
    #tratar el error cuando no hay conexion a mongo porque no funciona
    def __init__(self):
        self.client = None
        try:
            self.client = MongoClient("mongodb+srv://admin:admin@smartpark.oxbq8.mongodb.net/", serverSelectionTimeoutMS=5000)
            self.db = self.client["smartpark"]
            self.collection = self.db["estaciones"]
            self.isConnected = True
        except pymongo.errors.ConnectionFailure as e:
            self.isConnected = False
        except pymongo.errors.ServerSelectionTimeoutError as e:
            self.isConnected = False
        except pymongo.errors.ConfigurationError as e:
            self.isConnected = False
        except Exception as e:
            self.isConnected = False


    def conectar_mongo(self):
        try:
            self.client.admin.command('ping')
            self.isConnected = True
            return True
        except ConnectionFailure:
            self.isConnected = False
            return False
        except Exception as e:
            self.isConnected = False

    def read(self):
        datos = self.collection.find()
        for dato in datos:
            print(dato)

    def create(self, documento, cantidad):
        if cantidad == 1:
            resultado = self.collection.insert_one(documento)
            print(f"Documento insertado con ID: {resultado.inserted_id}")
            return resultado.inserted_id
        else:
            self.collection.insert_many(documento)
            print("Documentos insertados exitosamente!")

    def deleteone(self, filtro):
        res = self.collection.delete_one(filtro)
        if res.deleted_count > 0:
            return "Eliminado exitosamente"
        else:
            return "No se encontro ninguna coincidencia"

    def updateone(self, filtro, nuevo_valor):
        res = self.collection.update_one(filtro, nuevo_valor)
        if res.modified_count > 0:
            return True
        else:
            return False

    def findone(self, filtro, args=None):
        res = self.collection.find_one(filtro, args)
        if res:
            return res
        else:
            return False

    def aggregate(self, arg1):
        res =  self.collection.aggregate([arg1])
        return res


    def cerrar_conexion(self):
        self.client.close()

