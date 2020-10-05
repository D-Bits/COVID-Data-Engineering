"""
DAG for setting up the database, prior to ETL.
"""
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime
from os import getenv
import pandas as pd 


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 10, 1),
    "retries": 1,
}

dag = DAG("build_db", default_args=default_args, schedule_interval=None)

with dag: 

    # Get SQLA conn string
    conn = getenv("SQL_ALCHEMY_CONN")

    t1 = PostgresOperator(task_id="create_db", sql="sql/init.sql", postgres_conn_id=conn, database="airflow")
    t2 = PostgresOperator(task_id="create_tables", sql="sql/tables.sql", postgres_conn_id=conn, database="covid")

    t1 >> t2
