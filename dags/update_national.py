"""
Update summary of national data table.
"""
from os import getenv
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from requests import get
from os import remove
import pandas as pd
import psycopg2


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 10, 1),
    "retries": 1,
}

dag = DAG("update_national", default_args=default_args, schedule_interval="@daily")

def extract_transform(**context):

    data = get("https://api.covidtracking.com/v1/us/daily.json").json()

    # Drop undesired fields, ensure only the most recent record is written to db
    # Remove .head(n=1) for initial seeding of db
    df = pd.DataFrame(data, index=None).head(n=1).drop([
        'inIcuCurrently',
        'inIcuCumulative',
        'totalTestResults',
        'lastModified',
        'date',
        'hospitalizedCurrently',
        'total',
        'pending',
        'negative',
        'posNeg',
        'states',
        'negativeIncrease',
        'positiveIncrease',
        'totalTestResultsIncrease',
        'hash'
    ], axis=1)

    # Create an XCOM for this task to be used in load()
    context['ti'].xcom_push(key="df", value=df)


def load(**context):

    # Fetch the cleaned DataFrame from the above XCOM
    received_value = context["ti"].xcom_pull(key="df")

    # Fetch SQL Alchemy connection string from .env file
    db_conn = getenv("SQL_ALCHEMY_CONN")
    # Dump df to csv, and then load into db
    received_value.to_sql('nation_history', db_conn, index_label="id", schema='covid', method='multi', if_exists='append')


with dag:

    t1 = PythonOperator(task_id="extract_transform", python_callable=extract_transform, provide_context=True)
    t2 = PythonOperator(task_id="load", python_callable=load, provide_context=True)

    t1 >> t2
