import json
import os
import threading

detener_thread = True
guardar = False
aux = []
dic = {}

def verificar():  
    global guardar
    while detener_thread:
        if guardar:
            guardar = False

def modificar(temp):
    global guardar, aux
    aux.append(temp)
    guardar = True

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
    
        hilo = threading.Thread(target= verificar, args=() )
        hilo.start()

        if os.path.exists("respaldo.txt"):
            pass
        else:
            nombre = input("Ingrese el nombre: ")
            modificar(nombre)
            apellidos = input("Ingrese los apellidos: ")
            modificar(apellidos)
            tel = int(input("Ingrese numero de telefono: "))
            modificar(tel)
            edad = int(input("Ingrese la edad: "))
            modificar(edad)

        detener_thread = False
        hilo.join()

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