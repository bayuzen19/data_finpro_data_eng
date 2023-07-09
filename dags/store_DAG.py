from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.postgres_operator import PostgresOperator

from datacleaner import data_preparation_modelling
from modelling import modelling

yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2023, 7, 8),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG(
    'store_dag_final',
    default_args=default_args,
    schedule_interval=timedelta(days=30),
    template_searchpath=['/usr/local/airflow/sql_files'],
    catchup=True
) as dag:

    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id   = "postgres_localhost",
        sql='create_table.sql'
    )

    data_insert = PostgresOperator(
        task_id="data_ingestion",
        postgres_conn_id  = "postgres_localhost",
        sql='insert_into_table.sql'
    )

    data_cleaning = PostgresOperator(
        task_id="data_cleaning",
        postgres_conn_id  = "postgres_localhost",
        sql='data_cleaning.sql'
    )

    data_preparation_for_modelling = PythonOperator(
        task_id='data_preparation_modelling', 
        python_callable= data_preparation_modelling
    )

    modelling_evaluation = PythonOperator(
        task_id='modelling_evaluation', 
        python_callable=modelling
    )

create_table >> data_insert >> data_cleaning >> data_preparation_for_modelling >> modelling_evaluation