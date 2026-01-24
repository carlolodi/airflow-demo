from datetime import timedelta

import pendulum

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.sensors.time_delta import TimeDeltaSensor


@dag(
    dag_id="demo_04_sensors_reschedule_mode",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["demo", "sensors"],
)
def sensors_reschedule_mode():
    """A simple sensor example using reschedule mode.

    Sensors can either:
    - poke: occupy a worker slot while waiting
    - reschedule: free the worker slot between checks
    """

    start = EmptyOperator(task_id="start")

    wait_a_bit = TimeDeltaSensor(
        task_id="wait_15s",
        delta=timedelta(seconds=15),
        mode="reschedule",
        poke_interval=5,
    )

    end = EmptyOperator(task_id="end")

    start >> wait_a_bit >> end


sensors_reschedule_mode()
