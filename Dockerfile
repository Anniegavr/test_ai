# Use official Airflow image
FROM apache/airflow:2.9.0-python3.13

# Install additional Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs
COPY dags/ ${AIRFLOW_HOME}/dags/

# ===== docker-compose.yml =====
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  airflow:
    build: .
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
    command: webserver

  scheduler:
    build: .
    depends_on:
      - airflow
    volumes:
      - ./dags:/opt/airflow/dags
    command: scheduler

volumes:
  postgres_data: