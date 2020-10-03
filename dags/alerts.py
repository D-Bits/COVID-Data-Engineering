"""
Workflow to send an email anytime nationwide cases exceed a certain number.
"""
from os import getenv
from airflow import DAG
from airflow.utils.email import send_email
from airflow.operators.email_operator import send_email
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from emails.alert_bodies import cases_body, deaths_body
import pandas as pd


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 10, 1),
    "retries": 1,
}


dag = DAG("alerts", default_args=default_args, schedule_interval="@daily")


# Read data from "covid.nation_history" table
def extract(**context):

    # Get the SQL Alchemy connection string
    conn = getenv("SQL_ALCHEMY_CONN")
    # Get email address
    email = getenv("EMAIL_ADDRESS")
    # Load the "nation_history" table
    df = pd.read_sql_table('nation_history', conn, schema='covid', index_col='id')

    # Create an XCOM for this task to be used in alert_cases()
    context['ti'].xcom_push(key="df", value=df)
    context['ti'].xcom_push(key="email", value=email)


def alert_cases(**context):
    # Fetch the cleaned DataFrame from the above XCOM
    df = context["ti"].xcom_pull(key="df")
    email = context["ti"].xcom_pull(key="email")

    if int(df["positive"]) > 7000000:
        send_email(email, "U.S. Cases Exceed 7 million", cases_body)
    else:
        pass


def alert_deaths(**context):
    # Fetch the cleaned DataFrame from the above XCOM
    df = context["ti"].xcom_pull(key="df")
    email = context["ti"].xcom_pull(key="email")

    if int(df["death"] > 200000):
        send_email(email, "U.S. Cases Exceed 7 million", cases_body)
    else:
        pass


with dag:

    t1 = PythonOperator(task_id="alert_cases", python_callable=alert_cases, provide_context=True)