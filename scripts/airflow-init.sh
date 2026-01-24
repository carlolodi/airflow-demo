#!/usr/bin/env bash
set -euo pipefail

echo "[airflow-init] Migrating metadata DB..."
airflow db migrate

echo "[airflow-init] Creating admin user (idempotent)..."
airflow users create \
	--role Admin \
	--username "${_AIRFLOW_WWW_USER_USERNAME}" \
	--password "${_AIRFLOW_WWW_USER_PASSWORD}" \
	--firstname "${_AIRFLOW_WWW_USER_FIRSTNAME}" \
	--lastname "${_AIRFLOW_WWW_USER_LASTNAME}" \
	--email "${_AIRFLOW_WWW_USER_EMAIL}" \
	|| true

echo "[airflow-init] Creating default connections..."
airflow connections create-default-connections || true

echo "[airflow-init] Done. You can now start the scheduler and webserver."
