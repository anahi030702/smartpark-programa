from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class ConectionDb:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://admin:admin@smartpark.oxbq8.mongodb.net/", serverSelectionTimeoutMS=5000)
        self.db = self.client["smartpark"]
        self.collection = self.db["estaciones"]

    def conectar_mongo(self):
        try:
            self.client.admin.command('ping')
            return True
        except ConnectionFailure:
            return False

    def read(self):
        alumnos = self.collection.find()
        for alumno in alumnos:
            print(alumno)

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

    def updateone(self, filtro, nuevo_valor, array_filter = None):
        res = self.collection.update_one(filtro, nuevo_valor)
        if res.modified_count > 0:
            return "Documento actualizado exitosamente."
        else:
            return "No se encontró ningún documento que coincidiera con el criterio o no hubo cambios."

    def findone(self, filtro, cantidad):
        res = self.collection.find_one(filtro, cantidad)
        if res:
            print(res)
            return res
        else:
            print("No se encontró ningún documento que coincida con el criterio.")


    def cerrar_conexion(self):
        self.client.close()

