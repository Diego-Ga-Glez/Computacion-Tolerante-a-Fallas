from prefect import task, Flow
import json
import requests
import datetime

@task(max_retries=10, retry_delay=datetime.timedelta(seconds=10))
def extract(url):
    res = requests.get(url)
    return json.loads(res.content)

@task
def transform(datos):
    dic = {}
    lista = []

    if(len(datos) != 4):
        for i in datos:
            dic = {
                "ID_usuario" : i["userId"],
                "ID" : i["id"],
                "titulo" : i["title"],
                "completado" : i["completed"] 
            }
            lista.append(dic)
    else:
        dic = {
                "ID_usuario" : datos["userId"],
                "ID" : datos["id"],
                "titulo" : datos["title"],
                "completado" : datos["completed"] 
            }
        lista.append(dic)

    return lista

@task
def load(datos,path):
    with open(path, "w") as f:
        json.dump(datos,f, indent=4)

def etl_flow(dato):
    with Flow("etl_flow") as flow:
        e = extract("https://jsonplaceholder.cypress.io/todos" + dato)
        t = transform(e)
        load(t,"datos.json")

    return flow

while True:
    print()
    print("1. Extraer toda la informacion")
    print("2. Extraer un dato")
    opc = int(input(">>"))
    print()

    if opc == 1:
        flow = etl_flow("")
        flow.run()
    if opc == 2:
        aux = int(input("Ingrese un numero: "))  
        flow = etl_flow("/"+ str(aux))
        flow.run()









