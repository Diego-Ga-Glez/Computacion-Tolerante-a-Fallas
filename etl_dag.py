from airflow import DAG
import json
import requests
from datetime import datetime
from airflow.operators.python import PythonOperator

path = "/usr/local/lib/python3.8/dist-packages/airflow/example_dags"

def _extract(ti):
    res = requests.get("https://jsonplaceholder.cypress.io/todos")
    ti.xcom_push(key = 'dic1', value = json.loads(res.content))

def _extract_b(ti):
    res = requests.get("https://jsonplaceholder.typicode.com/users")
    ti.xcom_push(key = 'dic2', value = json.loads(res.content))

def _transform(ti):
    dic1 = ti.xcom_pull(key= 'dic1', task_ids='extract',)
    dic2 = ti.xcom_pull(key= 'dic2', task_ids='extract_b',)

    ti.xcom_push(key = 'dic3', value = dic1 + dic2)

def _load(ti):
    datos = ti.xcom_pull(key= 'dic3', task_ids='transform')

    with open(path + "/datos.json", "w") as f:
        json.dump(datos,f, indent=4)

with DAG(
    dag_id ="etl_dag",
    start_date= datetime(2022,1,1),
    schedule_interval=None,
    catchup=False,
    tags = ["airflow_etl_dag"]
) as dag:

    extract = PythonOperator( task_id="extract", python_callable = _extract)
    extract_b = PythonOperator( task_id = "extract_b", python_callable= _extract_b)
    transform = PythonOperator( task_id = "transform", python_callable= _transform)
    load = PythonOperator( task_id = "load", python_callable= _load)

[extract, extract_b] >> transform >> load