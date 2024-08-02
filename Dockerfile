FROM apache/airflow:2.9.3

# Switch to the "airflow" user
USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt