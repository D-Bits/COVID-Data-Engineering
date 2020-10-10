"""
Workflow to send an email anytime nationwide cases exceed a certain number.
"""
from os import getenv
from airflow import DAG
from airflow.utils.email import send_email
from airflow.operators.email_operator import send_email, EmailOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from emails.alert_bodies import cases_body, deaths_body
import pandas as pd


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 10, 1),
    "retries": 1,
}


dag = DAG("us_alerts", default_args=default_args, schedule_interval="@daily")


# Get email address
email = getenv("EMAIL_ADDRESS")

# Read data from "covid.nation_history" table
def extract(**context):

    # Get the SQL Alchemy connection string
    conn = getenv("SQL_ALCHEMY_CONN")
    # Load the "nation_history" table
    df = pd.read_sql_table('nation_history', conn, schema='usa')
    today = df.head(n=1)
    # Create an XCOM for this task to be used in alert_cases()
    context['ti'].xcom_push(key="df", value=today)


def alert_cases(**context):

    # Fetch the cleaned DataFrame from the above XCOM
    df = context["ti"].xcom_pull(key="df")
    # Send email if cases exceed 7 million
    cases = df['positive'] > 7000000

    if cases.bool():
        send_email(email, "U.S. Cases Exceed 7 million", cases_body)
    else:
        pass


def alert_deaths(**context):

    # Fetch the cleaned DataFrame from the above XCOM
    df = context["ti"].xcom_pull(key="df")
    email = context["ti"].xcom_pull(key="email")

    if df.head(n=1).loc[df['positive'] > 200000, 'More than 7 million cases'] == True:
        send_email(email, "U.S. Cases Exceed 7 million", cases_body)
    else:
        pass


with dag:
    
    t1 = PythonOperator(task_id="extract", python_callable=extract, provide_context=True)
    t2 = PythonOperator(task_id="alert_cases", python_callable=alert_cases, provide_context=True)
    t3 = PythonOperator(task_id="alert_deaths", python_callable=alert_deaths, provide_context=True)


# Execute tasks 2 and 3 in parallel, after task 1
t1 >> [t2, t3]