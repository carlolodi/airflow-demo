import pendulum

from airflow.decorators import dag, task


@dag(
    dag_id="demo_00_hello_taskflow",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["demo", "basics"],
)
def hello_taskflow():
    """A minimal TaskFlow DAG showing dependencies and XCom return values."""

    @task
    def extract() -> dict:
        return {"value": 42}

    @task
    def transform(data: dict) -> int:
        return int(data["value"]) * 2

    @task
    def load(result: int) -> None:
        print(f"Loaded result={result}")

    data = extract()
    result = transform(data)
    load(result)


hello_taskflow()
