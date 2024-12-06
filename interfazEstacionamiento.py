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
        if self.estacionamientos:
            print("Ya esta creado el estacionamiento")
            self.exit()
        else:
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

                self.exit()

    def editar_estacionamiento(self):
        dic = self.estacionamientos[0].dict()
        print({"nombre" : dic["nombre"], "ubicacion" : dic["ubicacion"] })
        clave = input("Escribe el nombre de la clave que deseas modificar :")
        new_valor = input("Escriba el nuevo valor que desea asignarle:")

        if self.db.conectar_mongo():
            self.db.updateone({"_id": ObjectId(self.estacionamientos[0].noEs)}, {"$set": {clave: new_valor}})

            dic[clave] = new_valor
            self.estacionamientos[0] = Estacionamiento(dic["no. estacionamiento"], dic["nombre"], dic["ubicacion"])
            self.estacionamientos.document(self.estacionamientos.dict())
            print("Valor actualizado correctamente!")
        else:
            dic[clave] = new_valor
            self.estacionamientos[0] = Estacionamiento(dic["no. estacionamiento"], dic["nombre"], dic["ubicacion"])
            self.estacionamientos.document(self.estacionamientos.dict())
            print("Los cambios se guardaron localmente hasta que se restablezca la conexion con la BD")

        self.exit()

    def exit(self):
        res = input("\nDesea regresar al menu principal? \n1.Si \n2.No\n")
        if res == "1":
            self.menu()
        elif res == "2":
            print("¡Hasta luego!")
        else:
            print("Opcion invalida")
            self.exit()


if __name__ == "__main__":
    interfazEstacionamiento().menu()