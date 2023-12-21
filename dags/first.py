from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import json
from airflow.exceptions import AirflowException
import logging
import os

default_args = {
    "owner": "niko",
    "depends_on_past": False,
    "start_date": datetime(2023, 12, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "example_dag",
    default_args=default_args,
    description="A simple example DAG",
    schedule_interval=timedelta(days=1),
)

start = DummyOperator(
    task_id="start",
    dag=dag,
)


def download_data():
    logging.info("Starting to download data from JSONPlaceholder")
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/todos")
        response.raise_for_status()
        logging.info("Data download completed successfully")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Data download failed: {e}")
        raise AirflowException(f"Data download failed: {e}")


download_data_task = PythonOperator(
    task_id="download_data",
    python_callable=download_data,
    dag=dag,
)


def process_data(**kwargs):
    task_instance = kwargs["ti"]
    data = task_instance.xcom_pull(task_ids="download_data")
    try:
        processed_data = [task for task in data if task["completed"]]
        return processed_data
    except TypeError as e:
        raise AirflowException(f"Error in processing data: {e}")


process_data_task = PythonOperator(
    task_id="process_data",
    python_callable=process_data,
    provide_context=True,
    dag=dag,
)


def save_data(**kwargs):
    task_instance = kwargs["ti"]
    data = task_instance.xcom_pull(task_ids="process_data")
    data_directory = "/opt/airflow/data"
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    try:
        filename = os.path.join(
            data_directory, f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(filename, "w") as file:
            json.dump(data, file)
        logging.info(f"Data saved successfully to {filename}")
    except Exception as e:
        logging.error(f"Error in saving data: {e}")
        raise AirflowException(f"Error in saving data: {e}")


save_data_task = PythonOperator(
    task_id="save_data",
    python_callable=save_data,
    provide_context=True,
    dag=dag,
)

end = DummyOperator(
    task_id="end",
    dag=dag,
)

start >> download_data_task >> process_data_task >> save_data_task >> end
