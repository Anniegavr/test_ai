from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import pandas as pd
import matplotlib.pyplot as plt

def extract_transform_load():
    hook = PostgresHook(postgres_conn_id='postgres_default')
    df = hook.get_pandas_df(sql='SELECT * FROM sales;')

    # Transform: parse dates, aggregate
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['month'] = df['sale_date'].dt.to_period('M')
    summary = df.groupby(['month', 'product'])['amount'].sum().reset_index()

    # Save summary
    summary.to_csv('/opt/airflow/dags/sales_summary.csv', index=False)

    # Plot total sales per month
    monthly = summary.groupby('month')['amount'].sum()
    plt.figure()
    monthly.plot(marker='o')
    plt.title('Total Sales by Month')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.tight_layout()
    plt.savefig('/opt/airflow/dags/plots/total_sales_by_month.png')
    plt.close()

    # Plot top products per month
    for m, group in summary.groupby('month'):
        plt.figure()
        group.set_index('product')['amount'].plot(kind='bar')
        plt.title(f'Sales by Product in {m}')
        plt.xlabel('Product')
        plt.ylabel('Amount')
        plt.tight_layout()
        plt.savefig(f'/opt/airflow/dags/plots/sales_{m}.png')
        plt.close()

with DAG(
    dag_id='sales_etl_and_viz',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    etl_and_visualize = PythonOperator(
        task_id='etl_and_viz',
        python_callable=extract_transform_load
    )