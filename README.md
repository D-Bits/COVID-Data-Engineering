
# About 

A data engineering project, built with Apache Airflow to monitor U.S. COVID-19 data

## Running Locally

**Prerequisites**

The following software must be installed before going further:

- Docker Desktop (v2.4.0.0, or higher)

**Environment Variables**

- First, create a `.env` file in the root of the project directory.
- Add the following environment variables to the file:

    - `LOAD_EX=n`
    - `EXECUTOR=Local`
    - `POSTGRES_USER=airflow`
    - `POSTGRES_PASSWORD=airflow`
    - `POSTGRES_DB=airflow`
    - `POSTGRES_HOST=postgres`
    - `POSTGRES_PORT=5432`
    - `SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow`