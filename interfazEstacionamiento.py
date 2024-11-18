from dns.name import empty

from estacionamiento import Estacionamiento
from sensor import Sensor
from bson import ObjectId
from conectToDb import ConectionDb


class interfazEstacionamiento:
    def __init__(self):
        self.sensores = Sensor()
        self.estacionamientos = Estacionamiento()
        self.estacionamientos.leer_doc()
        self.db = ConectionDb()

    def menu(self):
        print("MENU")
        print("1.Crear estacionamiento")
        print("2.Editar estacionamiento")
        print("3.Salir")
        res = input("Escribe el numero de la opcion que deseas: ")

        if res == "1":
            self.crear_estacionamiento()
        elif res == "2":
            self.editar_estacionamiento()
        elif res == "3":
            print("Saliendo...")
        else:
            print("Opcion invalida")
            self.menu()

    def crear_estacionamiento(self):
        print("Crear estacionamiento")
        nombre = input("Nombre del estacionamiento: ")
        ubicacion = input("Ubicacion del estacionamiento: ")
        print(nombre, ubicacion)
        res = input("¿Desea finalizar el registro del grupo? Escriba el numero que desea \n 1.Si \n 2.No \n ")

        if res == "1":
            #guardar el object id del estacionamiento que se cree como una propiedad que al cabo solo se usara 1 estacionamiento siempre
            estacionamiento = Estacionamiento("", nombre, ubicacion)
            print(estacionamiento)
            print("Estacionamiento creado exitosamente")

            if self.db.conectar_mongo():
                # self.updateDb()
                id_object = self.db.create(estacionamiento.dict(), 1)
                estacionamiento.noEs = str(id_object)
                self.estacionamientos.agregar(estacionamiento)
                self.estacionamientos.document(self.estacionamientos.dict())
            else:
                print("Actualmente no hay conexion con la BD. \nLa informacion creada sera guardada localmente hasta que se pueda establecer nuevamente comunicacion con la BD")
                self.estacionamientos.agregar(estacionamiento)
                self.estacionamientos.document(self.estacionamientos.dict())

    def updateDb(self):
        if self.sensores is not empty:
            #aqui debe ir una funcion que haga en connecttodb que haga un push a sensores dentro del documento estacionamiento
            print("Se restablecio la conexion con la BD y se subio la informacion guardada localmente!")
            #aqui tiene que ir una funcionn que vacie solo el arreglo de sensores en el archivo json
        else:
            print("No hay nada que mandar a la BD")

    def editar_estacionamiento(self):
        print("editar")


if __name__ == "__main__":
    interfazEstacionamiento().menu()