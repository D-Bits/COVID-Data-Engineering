"""
Workflow to send an email anytime nationwide cases exceed a certain number.
"""
from airflow import DAG
from airflow.operators.email_operator import EmailOperator, send_email
from datetime import datetime
import pandas as pd


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 10, 1),
    "retries": 1,
}


dag = DAG("alert_cases", default_args=default_args, schedule_interval="@daily")


# Read data from "covid.nation_history" table
def extract(**context):

    # Get the SQL Alchemy connection string

    df = pd.read_sql_table("nation_history", schema="covid")

