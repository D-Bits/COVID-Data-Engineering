"""
Workflow to send an email anytime nationwide cases exceed a certain number.
"""
from os import getenv
from airflow import DAG
from airflow.utils.email import send_email
from airflow.operators.email_operator import EmailOperator, send_email
from datetime import datetime
from emails.cases_alert import cases_body
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

    if df["positive"] > 7000000:
        send_email(email, "U.S. Cases Exceed 7 million", cases_body)
    else:
        pass
