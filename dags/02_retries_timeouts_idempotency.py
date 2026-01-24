from datetime import timedelta

import pendulum

from airflow.decorators import dag, task
from airflow.exceptions import AirflowFailException
from airflow.operators.python import get_current_context


@dag(
    dag_id="demo_02_retries_timeouts_idempotency",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["demo", "retries"],
)
def retries_timeouts_idempotency():
    """A task that fails on the first try and succeeds on retry.

    Run this DAG manually and watch the task retry.
    """

    @task(
        retries=2,
        retry_delay=timedelta(seconds=10),
        execution_timeout=timedelta(seconds=30),
    )
    def flaky_once_then_ok() -> str:
        context = get_current_context()
        ti = context["ti"]

        # try_number starts at 1 for the first attempt.
        if ti.try_number == 1:
            raise AirflowFailException(
                "Failing on first attempt to demonstrate retries"
            )

        return "Succeeded on retry"

    @task
    def print_result(message: str) -> None:
        print(message)

    print_result(flaky_once_then_ok())


retries_timeouts_idempotency()
