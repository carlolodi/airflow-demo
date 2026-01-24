import pendulum

from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup


@dag(
    dag_id="demo_09_task_groups_and_dynamic_mapping",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["demo", "taskgroup", "mapping"],
)
def task_groups_and_dynamic_mapping():
    """TaskGroups for UI organization + dynamic task mapping."""

    @task
    def get_items() -> list[str]:
        return ["alpha", "beta", "gamma"]

    @task
    def process(item: str) -> None:
        print(f"Processing item={item}")

    with TaskGroup(group_id="grouped"):
        items = get_items()
        process.expand(item=items)


task_groups_and_dynamic_mapping()
