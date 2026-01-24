import pendulum

from airflow.decorators import dag, task


@dag(
    dag_id="demo_01_scheduling_and_catchup",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="0 9 * * *",  # 09:00 UTC daily
    catchup=False,
    max_active_runs=1,
    tags=["demo", "scheduling"],
)
def scheduling_and_catchup():
    """Shows how schedule/start_date/catchup affect run creation.

    Tip: toggle catchup=True and watch the scheduler create backfill runs.
    """

    @task
    def show_context() -> None:
        # Many context values are available via Jinja templates too.
        # We keep it simple here to avoid parse-time side effects.
        print("This task runs once per DAG run.")

    show_context()


scheduling_and_catchup()
