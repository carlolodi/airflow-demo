# Airflow Demo (Beginner-Friendly)

This repository is a learning sandbox for **Apache Airflow** concepts.

Airflow is an **orchestrator**: it helps you define, schedule, run, and monitor *workflows* made of discrete steps (tasks). You describe workflows as code, and Airflow takes care of when and how they run.

## Quickstart (local Docker)

Prereqs: Docker Desktop (or any Docker engine with `docker compose`).

1. (Optional) Copy `.env.example` to `.env` and adjust values.
2. Initialize the Airflow metadata DB and create a local admin user:

	`docker compose up airflow-init`

3. Start the scheduler + web UI:

	`docker compose up -d`

4. Open the UI: http://localhost:8080

Default login (from `.env.example`): `admin` / `admin`.

## Do we need `requirements.txt`?

For this repo: **yes, but only for the Docker image**.

- Airflow itself is provided by the base image (`apache/airflow:...`).
- [requirements.txt](requirements.txt) is where you add *extra* Python deps/provider packages used by your DAGs (e.g., HTTP/Postgres providers).
- On Windows, installing Airflow directly with `pip` is usually painful; running via Docker is the simplest path.

To stop:

- `docker compose down`

To fully reset (deletes the Postgres volume/state):

- `docker compose down -v`

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

## Repo layout

- `dags/` — demo DAGs (workflow definitions)
- `data/` — local files used by dataset demos (mounted into containers)
- `logs/` — task logs (generated at runtime)
- `plugins/` — optional custom plugins/operators
- `scripts/` — helper scripts used by Docker Compose
- `docker-compose.yaml` — local Airflow stack (webserver + scheduler + Postgres)

## Demo DAGs (what to learn)

Each DAG is small on purpose; the goal is to isolate one idea at a time.

- `demo_00_hello_taskflow` ([dags/00_hello_taskflow.py](dags/00_hello_taskflow.py))
	- TaskFlow API, dependencies, XCom via return values
- `demo_01_scheduling_and_catchup` ([dags/01_scheduling_and_catchup.py](dags/01_scheduling_and_catchup.py))
	- `schedule`, `start_date`, `catchup`, run creation behavior
- `demo_02_retries_timeouts_idempotency` ([dags/02_retries_timeouts_idempotency.py](dags/02_retries_timeouts_idempotency.py))
	- retries, retry delay, timeouts, designing retry-safe tasks
- `demo_03_branching_and_trigger_rules` ([dags/03_branching_and_trigger_rules.py](dags/03_branching_and_trigger_rules.py))
	- branching, skipped tasks, joining branches with trigger rules
- `demo_04_sensors_reschedule_mode` ([dags/04_sensors_reschedule_mode.py](dags/04_sensors_reschedule_mode.py))
	- sensors, `poke` vs `reschedule` mode, worker-slot usage
- `demo_06_dataset_producer` ([dags/06_dataset_producer.py](dags/06_dataset_producer.py))
	- datasets (data-aware scheduling): producing dataset events
- `demo_07_dataset_consumer` ([dags/07_dataset_consumer.py](dags/07_dataset_consumer.py))
	- datasets: triggering a DAG when a dataset updates
- `demo_08_variables_and_templating` ([dags/08_variables_and_templating.py](dags/08_variables_and_templating.py))
	- Variables + Jinja templating with common context values
- `demo_09_task_groups_and_dynamic_mapping` ([dags/09_task_groups_and_dynamic_mapping.py](dags/09_task_groups_and_dynamic_mapping.py))
	- TaskGroups (UI organization) + dynamic task mapping

## Suggested exercises

1. Trigger each DAG manually and inspect logs + graph view.
2. In the UI, set Variable `demo_message` and rerun `demo_08_variables_and_templating`.
3. Run `demo_06_dataset_producer` and watch `demo_07_dataset_consumer` trigger.