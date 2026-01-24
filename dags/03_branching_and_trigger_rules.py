import pendulum

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule


@dag(
    dag_id="demo_03_branching_and_trigger_rules",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["demo", "branching"],
)
def branching_and_trigger_rules():
    """Branching creates SKIPPED tasks; trigger rules control joins.

    Trigger this DAG with conf like:
    {
      "path": "a"
    }
    """

    start = EmptyOperator(task_id="start")

    def choose_path(**context):
        conf = (context.get("dag_run").conf or {}) if context.get("dag_run") else {}
        return "path_a" if conf.get("path", "a") == "a" else "path_b"

    branch = BranchPythonOperator(task_id="branch", python_callable=choose_path)

    path_a = EmptyOperator(task_id="path_a")
    path_b = EmptyOperator(task_id="path_b")

    join = EmptyOperator(
        task_id="join",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    end = EmptyOperator(task_id="end")

    start >> branch
    branch >> [path_a, path_b]
    [path_a, path_b] >> join >> end


branching_and_trigger_rules()
