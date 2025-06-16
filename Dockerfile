# Use official Airflow image
FROM apache/airflow:2.9.0-python3.13

# Install additional Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs
COPY dags/ ${AIRFLOW_HOME}/dags/