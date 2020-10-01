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

def etl():

    data = get("https://api.covidtracking.com/v1/us/daily.json").json()

    # Drop undesired fields, ensure only the most recent record is written to db
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

    # Fetch SQL Alchemy connection string from .env file
    db_conn = getenv("SQL_ALCHEMY_CONN")
    
    # Dump df to csv, and then load into db
    df.to_sql('nation_history', db_conn, index_label="id", schema='covid', if_exists='append')

with dag:

    t1 = PythonOperator(task_id="etl", python_callable=etl)
