import json
import os

dic = {}

try:
    archivo = open('datos.json')
    dic = json.loads(archivo.read())
    archivo.close()
except:
    pass

num = 0

while num != 4:
    print ("\n1.- Agregar una contacto") 
    print ("2.- Mostrar contactos")
    print ("3.- Borrar agenda")
    print ("4.- Salir\n")
    
    num = int(input("Ingrese una opcion: "))
    print()

    if num == 1:
        nombre = input("Ingrese el nombre: ")
        apellidos = input("Ingrese los apellidos: ")
        tel = int(input("Ingrese numero de telefono: "))
        edad = int(input("Ingrese la edad: "))

        dic[nombre] = {
            "APELLIDOS": apellidos,
            "TELEFONO": tel,
            "EDAD": edad
        }

        aux = open('datos.json', 'w')
        json.dump(dic, aux, indent=4)
        aux.close()

    elif num == 2:
        for llave, valor in dic.items():
            print("Nombre: " + str(llave))
            lista = list(valor.values())
            print("Apellido: " + str(lista[0]))
            print("Telefono: " + str(lista[1]))
            print("Edad: " + str(lista[2]))
            print()

    elif num == 3:
        os.remove("datos.json")
        dic.clear()