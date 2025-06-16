# Use official Airflow image
FROM apache/airflow:3.0.2
# Install additional Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs
COPY dags/ ${AIRFLOW_HOME}/dags/