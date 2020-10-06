
# About 

A data engineering project, built with Apache Airflow to monitor COVID-19 data.

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
    - `SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/covid`
    - `EMAIL_ADRESS=(your email address)`

**Bootstraping**

- Run `docker-compose up -d --build` to bootstrap servers.
- Navigate to `localhost:8080` in your browser.
- Under the `Admin` menu, select `Connections`.
- Click `Create`.
- Enter the following values for the fields:

    - `Conn Id`: A name for to connection to the containerized Postgres instance (Ex: "*postgres_main*").
    - `Conn Type`: Postgres
    - `Host`: postgres
    - `Schema`: public
    - `Login`: (DB username)
    - `Password`: (DB password)
    - `Port`: 5432

**Initializing the DB**

Once you have Postgres added to `Connections`, you can then run the `build_db` DAG to create the database, along with the appropriate schemas and tables.

## DAG Descriptions

- `build_db`: To create the database, and tables for it. Run this before all other DAGs.
- `update_states`: Update state-specific data for all U.S. states and territories.
- `update_us_national`: Update nation-wide data for the United States.