import pendulum

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.bash import BashOperator


@dag(
    dag_id="demo_08_variables_and_templating",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["demo", "templating", "variables"],
)
def variables_and_templating():
    """Shows Variables (runtime config) and Jinja templating."""

    @task
    def get_message() -> str:
        # Avoid Variable.get at import time; do it in a task.
        return Variable.get("demo_message", default_var="Hello from Airflow Variables!")

    message = get_message()

    echo_context = BashOperator(
        task_id="echo_context",
        bash_command=(
            "echo 'ds={{ ds }}' && "
            "echo 'run_id={{ run_id }}' && "
            "echo 'message={{ ti.xcom_pull(task_ids=\"get_message\") }}'"
        ),
    )

    message >> echo_context


variables_and_templating()
