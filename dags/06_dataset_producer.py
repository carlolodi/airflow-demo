from datetime import datetime

import pendulum

from airflow.datasets import Dataset
from airflow.decorators import dag, task


demo_dataset = Dataset("file:///opt/airflow/data/demo_dataset.txt")


@dag(
    dag_id="demo_06_dataset_producer",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["demo", "datasets"],
)
def dataset_producer():
    """Produces a Dataset event and writes a local file.

    The file is mounted from ./data into the container at /opt/airflow/data.
    """

    @task(outlets=[demo_dataset])
    def write_dataset_file() -> str:
        path = "/opt/airflow/data/demo_dataset.txt"
        line = f"produced_at={datetime.utcnow().isoformat()}Z\n"
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(line)
        return path

    write_dataset_file()


dataset_producer()
