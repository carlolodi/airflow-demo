# Airflow Demo (Beginner-Friendly)

This repository is a learning sandbox for **Apache Airflow** concepts.

Airflow is an **orchestrator**: it helps you define, schedule, run, and monitor *workflows* made of discrete steps (tasks). You describe workflows as code, and Airflow takes care of when and how they run.

## What Apache Airflow is (and isn’t)

**Airflow is great for**:

- Scheduling recurring jobs (hourly, daily, etc.)
- Coordinating multi-step pipelines (ETL/ELT, ML training, reports)
- Tracking status, logs, retries, and dependencies between steps

**Airflow is not**:

- A data processing engine (Spark/DBT/etc. do the work; Airflow coordinates)
- A general-purpose message queue
- A place to run infinite/always-on services (tasks should be bounded)

## Mental model

Airflow revolves around a few core ideas:

1. **You write a DAG**: a Python file that declares tasks and dependencies.
2. **The scheduler creates runs**: based on the DAG’s schedule and time window.
3. **Workers execute tasks**: tasks run in isolated processes/containers depending on your executor.
4. **Everything is tracked**: the metadata database stores DAG runs, task instances, retries, and more.

## Key concepts beginners should know

### DAG (Directed Acyclic Graph)

A **DAG** is a workflow definition.

- “Directed”: tasks have an order via dependencies
- “Acyclic”: no loops (a task can’t depend on itself transitively)
- A DAG is *a definition*, not a single run

### Tasks, Operators, and TaskFlow

- A **task** is one step in the workflow.
- An **operator** is a template for a task (e.g., run Python, execute SQL, call a Bash command).
- **TaskFlow API** (decorators like `@dag` / `@task`) is a modern, pythonic way to write tasks.

Rule of thumb: keep tasks **small, idempotent, and retryable**.

### DAG Run, Task Instance

- A **DAG run** is one execution of a DAG for a specific time interval.
- A **task instance** is one execution attempt of a task within a particular DAG run.

If you remember one thing: *Airflow tracks work at the task-instance level.*

### Scheduling: `start_date`, `schedule`, “logical date”

Scheduling is the part that surprises most newcomers.

- `start_date` says when the schedule can begin.
- `schedule` (cron or presets like `@daily`) determines run frequency.
- Airflow triggers runs for **data intervals**; historically people called this the **execution date** or **logical date**.

Common gotcha: with schedules, the run label often refers to the *start of the data interval*, not “when it actually ran”.

### `catchup` and backfills

- If `catchup=True`, Airflow may create many historical runs from `start_date` up to now.
- Backfilling means running past intervals on purpose.

For learning and small demos, many people set `catchup=False` to avoid surprise run explosions.

### Dependencies and trigger rules

- Dependencies like `task_a >> task_b` define order.
- **Trigger rules** control when a downstream task runs (e.g., only if all upstream succeeded, or if any succeeded).

### Retries, timeouts, and idempotency

Airflow assumes tasks can fail and be retried.

- Use retries for transient failures (network, flaky APIs).
- Use timeouts to prevent stuck tasks.
- Design tasks to be **idempotent** (safe to run again).

### XCom (cross-communication)

**XCom** allows tasks to pass small pieces of metadata.

- Good for IDs, small strings, status flags
- Not good for large payloads (use object storage, databases, etc.)

### Connections, Variables, and Secrets

- **Connections**: credentials/endpoints for external systems (databases, APIs).
- **Variables**: simple runtime configuration.
- In production, both are often backed by a secrets manager.

### Templating (Jinja)

Many fields support Jinja templating so you can reference run context (dates, params, etc.).

This is how you generate date-partitioned paths like “process data for {{ ds }}”.

### Scheduler, Webserver, Metadata DB, Executor

These are the moving parts you’ll hear about constantly:

- **Webserver**: UI for browsing DAGs, runs, logs
- **Scheduler**: decides what should run, and when
- **Metadata DB**: stores state (runs, task instances, retries, etc.)
- **Executor**: decides *where/how* tasks execute
	- `SequentialExecutor` (simple, one task at a time)
	- `LocalExecutor` (parallel on one machine)
	- `CeleryExecutor` / `KubernetesExecutor` (distributed)

## Practical best practices (early on)

- Prefer many small tasks over one huge task.
- Keep tasks deterministic and avoid hidden shared state.
- Don’t “compute inside the scheduler parse”: DAG files should be fast to import.
- Log clearly; logs are your primary debugging tool.
- Treat Airflow as orchestration glue: delegate heavy compute to purpose-built systems.

## How to use this repo

This repo is intended to contain simple example DAGs and configuration as you learn.

Suggested structure (as you grow it):

- `dags/` — DAG definitions
- `plugins/` — custom operators/hooks (optional)
- `docker-compose.yaml` — local Airflow (common for demos)

If you add a local docker setup, consider documenting:

- How to start Airflow (`docker compose up`)
- Where the UI runs (usually `http://localhost:8080`)
- Default credentials (if any)

## Next steps

Good beginner exercises:

1. Create a “hello world” DAG with two tasks and a dependency.
2. Add retries and a deliberate failure to see task states.
3. Experiment with `catchup` and see how many runs get created.
4. Use XCom for a small value; use a file/DB for large data.

---

If you’d like, tell me how you plan to run Airflow for this demo (Docker Compose? Astronomer? local `pip install apache-airflow`?), and I can tailor this README with exact startup steps and a first example DAG.