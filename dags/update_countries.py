"""
DAG to update socio-economic, and non-covid health data for countries
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from requests import get
from os import getenv
import pandas as pd


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 10, 1),
    "retries": 1,
}

dag = DAG("update_countries", default_args=default_args, schedule_interval="@yearly")


def extract(**context):

    data = get("https://covid.ourworldindata.org/data/owid-covid-data.json").json()
    # Create an XCOM for this task to be used in transform()
    context['ti'].xcom_push(key="data", value=data)


def transform(**context):

    # Fetch the JSON data from the above XCOM
    data = context["ti"].xcom_pull(key="data")

    df = pd.DataFrame(data)
    # Invert the axis of the DataFrame
    df = df.drop(['data']).transpose()
    # Create an XCOM for this task to be used in load()
    context['ti'].xcom_push(key="df", value=df)


def load(**context):

    df = context["ti"].xcom_pull(key="df")
    # Fetch SQL Alchemy connection string from .env file
    db_conn = getenv("SQL_ALCHEMY_CONN")
    # Dump df to csv, and then load into db
    df.to_sql(
        'countries', 
        db_conn, 
        index=False, 
        schema='world', 
        method='multi', 
        if_exists='replace',
    )


with dag:

    t1 = PythonOperator(task_id="extact", python_callable=extract, provide_context=True)
    t2 = PythonOperator(task_id="transform", python_callable=transform, provide_context=True)
    t3 = PythonOperator(task_id="load", python_callable=load, provide_context=True)

    t1 >> t2 >> t3
