# Use the Apache Airflow 2.9.1 image as the base image
FROM apache/airflow:2.9.1

# Switch to the "airflow" user
USER airflow

# Install pip
RUN curl -O 'https://bootstrap.pypa.io/get-pip.py' && \
    python3 get-pip.py

# Install libraries from requirements.txt
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
