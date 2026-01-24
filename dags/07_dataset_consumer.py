import pendulum

from airflow.datasets import Dataset
from airflow.decorators import dag, task


demo_dataset = Dataset("file:///opt/airflow/data/demo_dataset.txt")


@dag(
    dag_id="demo_07_dataset_consumer",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=[demo_dataset],
    catchup=False,
    tags=["demo", "datasets"],
)
def dataset_consumer():
    """Runs when the producer updates the dataset."""

    @task
    def read_last_lines() -> None:
        path = "/opt/airflow/data/demo_dataset.txt"
        try:
            with open(path, "r", encoding="utf-8") as handle:
                lines = handle.readlines()
        except FileNotFoundError:
            lines = []

        print(f"Dataset file: {path}")
        print("Last 5 lines:")
        for line in lines[-5:]:
            print(line.rstrip("\n"))

    read_last_lines()


dataset_consumer()
