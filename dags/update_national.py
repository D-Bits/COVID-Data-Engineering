"""
Update summary of national data table.
"""
from os import getenv
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from requests import get
import pandas as pd
import psycopg2


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 9, 29),
    "retries": 1,
}

dag = DAG("update_national", default_args=default_args, schedule_interval=None)

def etl():

    data = get("https://api.covidtracking.com/v1/us/daily.json").json()

    df = pd.DataFrame(data).drop([
        'inIcuCurrently',
        'inIcuCumulative',
        'totalTestResults',
        'lastModified',
        'dateChecked',
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



    # Connect to db
    conn = psycopg2.connect(
        dbname="airflow",
        user='airflow',
        password='airflow',
        host='postgres',
        port=5432
    )
    
    with conn.cursor() as curs:
        # Call a stored proc on the server to update the table
        curs.callproc(
            "sp_update_nation_history", [
                (df['date']),
                df['positive'],
                df['death'],
                df['deathIncrease'],
                df['recovered'],
                df['hospitalizedCurrently'],
                df['hospitalizedCumulative'],
                df['onVentilatorCurrently'],
                df['onVentilatorCumulative']
            ]
        )
    # Commit the transaction to the db, and close the connection
    curs.commit()
    curs.close()

with dag:

    t1 = PythonOperator(task_id="etl", python_callable=etl)
