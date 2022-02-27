import json
import os
import threading
import pickle
import psutil

detener_thread = True
guardar = False
aux = []
dic = {}
campos = ["nombre", "apellidos", "telefono", "edad"]

def verificar():  
    global guardar
    while detener_thread:
        if guardar:
            with open("respaldo.pickle", "wb") as archivo:
                pickle.dump(aux, archivo)

            guardar = False
            archivo.close()

def modificar(temp):
    global guardar, aux
    aux.append(temp)
    guardar = True


if os.path.exists('datos.json'):
    archivo = open('datos.json')
    dic = json.loads(archivo.read())
    archivo.close()

num = 0

while num != 5:
    print ("\n1.- Agregar una contacto") 
    print ("2.- Mostrar contactos")
    print ("3.- Borrar agenda")
    print ("4.- Desactivar prolocker")
    print ("5.- Salir\n")
    
    num = int(input("Ingrese una opcion: "))
    print()

    if num == 1:          
        aux.clear()
        
        detener_thread = True
        hilo = threading.Thread(target= verificar)
        hilo.start()

        if os.path.exists("respaldo.pickle"):
            with open("respaldo.pickle", "rb") as archivo:
                aux = pickle.load(archivo)

            temp = len(aux)

            for i in range(temp):
                print("Ingrese "+ campos[i] + ": " + str(aux[i]))
            
            cont = 4-temp

            for i in range(4-temp):
                var = input("Ingrese " + campos[4-(cont)] + ": ")
                cont -= 1
                aux.append(var)
 
        else:
            temp = input("Ingrese nombre: ")
            modificar(temp)

            temp = input("Ingrese apellidos: ")
            modificar(temp)

            temp= input("Ingrese telefono: ")
            modificar(temp)

            temp = input("Ingrese edad: ")
            modificar(temp)


        os.remove("respaldo.pickle")

        detener_thread = False
        hilo.join()

        dic[aux[0]] = {
             "APELLIDOS": aux[1],
             "TELEFONO": aux[2],
             "EDAD": aux[3] }

        archivo_js = open('datos.json', 'w')
        json.dump(dic, archivo_js, indent=4)
        archivo_js.close()

    elif num == 2:
        for llave, valor in dic.items():
            print("Nombre: " + str(llave))
            lista = list(valor.values())
            print("Apellido: " + str(lista[0]))
            print("Telefono: " + str(lista[1]))
            print("Edad: " + str(lista[2]))
            print()

    elif num == 3:
        if os.path.exists("datos.json"):
            os.remove("datos.json")

        if os.path.exists("respaldo.pickle"):
            os.remove("respaldo.pickle")

        dic.clear()

    elif num == 4:
        for proc in psutil.process_iter():
            if proc.name().lower() == "python.exe":
                proc.kill()