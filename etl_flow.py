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
    lista = []

    for i in datos:
        lista.append({
            "ID_usuario" : i["userId"],
            "ID" : i["id"],
            "titulo" : i["title"],
            "completado" : i["completed"] 
            })

    return lista

@task
def load(datos,path):
    with open(path, "w") as f:
        json.dump(datos,f, indent=4)

def etl_flow():
    with Flow("etl_flow") as flow:
        e = extract("https://jsonplaceholder.cypress.io/todos")
        t = transform(e)
        load(t,"datos.json")

    return flow


flow = etl_flow()
flow.run()
    









