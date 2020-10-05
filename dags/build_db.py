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

    t1 = PostgresOperator(task_id="create_db", sql="CREATE DATABASE covid;", postgres_conn_id='postgres_main', database="airflow", autocommit=True)
    t2 = PostgresOperator(task_id="create_world_schema", sql="CREATE SCHEMA world;", postgres_conn_id='postgres_main', database="covid", autocommit=True)
    t3 = PostgresOperator(task_id="create_usa_schema", sql="CREATE SCHEMA usa;", postgres_conn_id='postgres_main', database="covid", autocommit=True)
    t4 = PostgresOperator(task_id="create_tables", sql="sql/tables.sql", postgres_conn_id='postgres_main', database="covid", autocommit=True)

    t1 >> t2 >> t3 >> t4
