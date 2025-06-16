# Airflow Dockerized App

## New: Sales Database Initialization
We now auto-create a `sales_db` database and `sales` table at Postgres startup via the SQL script in `db_init/init_sales_db.sql`.

## Setup & Running
1. Ensure your working directory is the project root.
2. Build images:
   ```bash
   docker compose build --no-cache
   ```
3. Launch services (initializes behind the scenes):
   ```bash
   docker compose up -d --remove-orphans
   ```
   - This runs Postgres (creating `airflow` and `sales_db`), then starts Airflow web and scheduler.
4. Verify Airflow metadata DB is migrated automatically.
5. Use Airflow UI at http://localhost:8080 (login: `admin` / `admin`).
6. Confirm `sales_db` table exists:
   ```bash
   psql -h localhost -U airflow -d sales_db -c '\\dt'
   ```

## Updating Containers with New Changes
On code or config changes (DAGs, Dockerfile, SQL scripts):

1. **Rebuild images**:
   ```bash
   docker compose build --no-cache
   ```
2. **Restart services**:
   ```bash
   docker compose up -d --remove-orphans
   ```
3. **(If DB init changed)** Recreate volume:
   ```bash
   docker compose down --volumes
   docker compose up -d
   ```
4. **Check logs**:
   ```bash
   docker compose logs -f airflow-web postgres
   ```

## Podman Alternative
Alias or use:
```bash
podman-compose build --no-cache
podman-compose up -d --remove-orphans
podman-compose down --volumes
```

---

## Troubleshooting UI Access from WSL

If you still can’t reach `http://localhost:8080` or other service ports from Windows when running in WSL:

1. **Ensure Docker Desktop WSL integration is enabled**
   - Open Docker Desktop → Settings → Resources → WSL Integration. Enable your distro.

2. **Verify port binding**
   - In WSL, run:
     ```bash
     docker compose ps
     ```
     Confirm the `0.0.0.0:8080->8080/tcp` mapping for `airflow-web`.

3. **Access via Windows localhost**
   - From Windows browser, use `http://localhost:8080`, **not** the WSL IP.

4. **Check Windows Firewall**
   - Ensure Docker Desktop is allowed through the firewall for incoming connections on the relevant ports.

5. **Test with curl**
   - From Windows CMD or PowerShell:
     ```powershell
     curl http://localhost:8080/health
     ```
     You should see a JSON health response.

6. **Alternative: use Portainer**
   - If Docker Desktop is not available, deploy Portainer in WSL to get a web UI:
     ```bash
     docker run -d -p 9000:9000 \
       --name portainer \
       --restart=always \
       -v /var/run/docker.sock:/var/run/docker.sock \
       portainer/portainer-ce
     ```
   - Then browse to `http://localhost:9000` to manage containers.

---

## Viewing Your Running Apps & Services

Once your stack is up, you can inspect and use the components:

1. **List running containers**
   ```bash
   docker compose ps
   ```
   This shows `postgres`, `airflow-web`, and `scheduler` status.

2. **Airflow UI**
   Visit http://localhost:8080 in your browser to view and trigger DAGs.

3. **Airflow CLI** (optional)
   ```bash
   docker compose exec airflow-web airflow dags list
   ```
   Lists all available DAGs from your `dags/` folder.

4. **Inspect logs**
   ```bash
   docker compose logs -f airflow-web scheduler
   ```
   Streams real‑time logs from the webserver and scheduler.

5. **Sales output files**
   To review your ETL artifacts and plots:
   - **CSV summary**: in `dags/sales_summary.csv` on the host (or exec into the container).
   - **Plots**: in `dags/plots/total_sales_by_month.png` and `dags/plots/sales_<month>.png`.

6. **Postgres shell**
   ```bash
   docker compose exec postgres psql -U airflow -d sales_db
   select * from sales limit 10;
   ```
   Query raw sales data interactively.

---
