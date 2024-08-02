from airflow import DAG,AirflowException
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import random
import time

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
dag = DAG(
    'random_exception_dag',
    default_args=default_args,
    description='A simple DAG that throws an exception randomly',
    schedule_interval='*/2 * * * *',
    catchup=False,
)

# Define the Python function that throws an exception randomly
def random_exception():
    random.seed(time.time())
    if random.random() < 0.2:
        raise AirflowException("This is a random exception")
    else:
        print("Task completed successfully")

# Define the PythonOperator
random_exception_task = PythonOperator(
    task_id='random_exception_task',
    python_callable=random_exception,
    dag=dag,
)

# Define the task dependencies
random_exception_task
