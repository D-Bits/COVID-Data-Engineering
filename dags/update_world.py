"""
DAG to update global data.
"""
from os import getenv
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy.types import TIMESTAMP, VARCHAR
from requests import get
from os import remove
import pandas as pd
import psycopg2


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 10, 1),
    "retries": 1,
}

dag = DAG("update_world", default_args=default_args, schedule_interval="@daily")


# To be used with df.to_sql()
data_types = {
    "Date": TIMESTAMP(),
    "CountryCode": VARCHAR(length=2),
    "Country": VARCHAR(length=255),
}

def extract_transform(**context):

    data = get("https://api.covid19api.com/summary").json()

    df = pd.DataFrame(data["Countries"], index=None)
    # Clean data
    cleaned_data = df.drop([
        "Slug",
        "Premium"
    ], axis=1)

    # Create an XCOM for this task to be used in load()
    context['ti'].xcom_push(key="df", value=cleaned_data)


def load(**context):

    df = context["ti"].xcom_pull(key="df")
    # Fetch SQL Alchemy connection string from .env file
    db_conn = getenv("SQL_ALCHEMY_CONN")
    # Dump df to csv, and then load into db
    df.to_sql(
        'global_summary', 
        db_conn, 
        index=False, 
        schema='world', 
        method='multi', 
        if_exists='replace',
        dtype=data_types
    )


with dag:

    t1 = PythonOperator(task_id="extract_transform", python_callable=extract_transform, provide_context=True)
    t2 = PythonOperator(task_id="load", python_callable=load, provide_context=True)

    t1 >> t2