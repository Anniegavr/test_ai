from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import psycopg2

def check_db_running():
    try:
        conn = psycopg2.connect(
            host='postgres',
            dbname='airflow',
            user='airflow',
            password='airflow',
            port=5432
        )
        conn.close()
        print("Database is running.")
    except Exception as e:
        raise RuntimeError(f"Database check failed: {e}")

with DAG(
    dag_id='db_health_check',
    start_date=days_ago(1),
    schedule_interval='@hourly',
    catchup=False
) as dag:

    health_check = PythonOperator(
        task_id='check_postgres',
        python_callable=check_db_running
    )