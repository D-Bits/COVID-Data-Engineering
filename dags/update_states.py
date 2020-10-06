"""
DAG to update current data for U.S. States and territories
"""
from os import getenv
from requests import get
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd 


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 10, 1),
    "retries": 1,
}

dag = DAG('update_states', default_args=default_args, schedule_interval="@daily")


def extract(**context):

    data = get("https://api.covidtracking.com/v1/states/current.json").json()

    # Create an XCOM for this task to be used in load()
    context['ti'].xcom_push(key="data", value=data)


def transform(**context):

    # Fetch the JSON data from the above XCOM
    data = context["ti"].xcom_pull(key="data")

    df = pd.DataFrame(data, index=None).drop([
        'deathConfirmed',
        'deathProbable',
        'totalTestEncountersViral',
        'totalTestsPeopleViral',
        'totalTestsAntibody',
        'positiveTestsAntibody',
        'negativeTestsAntibody',
        'totalTestsPeopleAntibody',
        'positiveTestsPeopleAntibody',
        'negativeTestsPeopleAntibody',
        'totalTestsPeopleAntigen',
        'positiveTestsPeopleAntigen',	
        'totalTestsAntigen',	
        'positiveTestsAntigen',
        'pending',
        'totalTestResults',
        'dateModified',
        'commercialScore',	
        'negativeRegularScore',
        'negativeScore',	
        'positiveScore',	
        'score',	
        'grade',
        'dataQualityGrade',
        'negative',
        'fips',
        'totalTestResultsSource',
        'onVentilatorCumulative',
        'positiveTestsViral',
        'negativeTestsViral',
        'positiveCasesViral',
        'total',
        'date',
        'hash'
    ], axis=1)

    # Drop duplicate dates
    df.drop_duplicates(subset=['dateChecked'])

    # Create an XCOM for this task to be used in load()
    context['ti'].xcom_push(key="df", value=df)


def load(**context):

    # Fetch the cleaned DataFrame from the above XCOM
    df = context["ti"].xcom_pull(key="df")

    # Fetch SQL Alchemy connection string from .env file
    db_conn = getenv("SQL_ALCHEMY_CONN")
    # Dump df to csv, and then load into db
    df.to_sql(
        'states_current', 
        db_conn, 
        index=False, 
        schema='usa', 
        method='multi', 
        if_exists='replace'
    )


with dag:

    t1 = PythonOperator(task_id='extract', python_callable=extract, provide_context=True)
    t2 = PythonOperator(task_id='transform', python_callable=transform, provide_context=True)
    t3 = PythonOperator(task_id='load', python_callable=load, provide_context=True)

    t1 >> t2 >> t3
