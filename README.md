# 🚀 Apache Airflow 3.0 Data USA Population Pipeline

A containerized, production-ready data pipeline built on **Apache Airflow 3.0** to extract, transform, and load U.S. population records from the Data USA API into both structured CSV files and a PostgreSQL database.

---

## 📐 Pipeline Architecture

```mermaid
graph TD
    API[Data USA Public API] -->|JSON Records| DAG_Extract[extract_task]
    DAG_Extract -->|Raw Data| DAG_Transform[transform_task]
    DAG_Transform -->|Transformed JSON| Load_CSV[load_task]
    DAG_Transform -->|Transformed JSON| Load_DB[load_db_task]
    
    Load_CSV -->|Writes File| CSV_Disk[(Local CSV Files)]
    Load_DB -->|Postgres Hook| PG_DB[(PostgreSQL Database)]

    subgraph scripts [Scripts Layer]
        extract_api.py
        transform_data.py
        save_csv.py
        save_db.py
    end
    
    subgraph dags [Orchestration Layer]
        dag.py
    end
```

---

## ✨ Features & Achievements

*   **Airflow 3.0 Task SDK**: Implements decoupled, forward-compatible DAG design utilizing `@dag` and `@task` decorators from `airflow.sdk`.
*   **Parallel Execution**: The pipeline splits into parallel branches to save output to disk and dump directly to the database.
*   **Database Ingestion Engine**: Automatically creates the Postgres database schema if the table is absent and appends data seamlessly using Pandas `to_sql()`.
*   **Secure Environment Configuration**: Uses a local `.env` file to manage sensitive Airflow credentials (e.g. `FERNET_KEY` and connection URIs) securely, bypassing version control via `.gitignore`.
*   **Data Enrichment**:
    *   Converts all string values and column headers to lowercase for uniform processing.
    *   Injects audit fields (`inserted_on` as current date, `source_name` as `"test"`).
    *   Saves output to timestamped CSV files (`datausa_population_YYYYMMDD_HHMMSS.csv`).

---

## 📁 Repository Structure

```text
Apache Airflow 1.0/
├── config/
│   └── airflow.cfg         # Airflow configuration file
├── dags/
│   ├── dag.py              # Main Orchestrated DAG Pipeline
│   └── db.py               # Database connection test DAG
├── data/                   # Generated output CSV files
├── logs/                   # Celery & DAG Processor execution logs
├── scripts/                # Modular execution layer
│   ├── extract_api.py      # Extract data from Data USA API
│   ├── save_csv.py         # Timestamped CSV generator
│   ├── save_db.py          # PostgreSQL ingestion script (append mode)
│   └── transform_data.py   # Lowercase values/columns & audit injection
├── .env                    # Secret environment configs (Git ignored)
├── .gitignore              # Tells git which files to ignore
├── docker-compose.yaml     # Multicontainer setup (Postgres, Redis, Airflow)
└── pyproject.toml          # Project package definitions
```

---

## 🛠️ Getting Started & Commands

### Prerequisites
*   Docker & Docker Compose
*   Python 3.12+ (managed with `uv` or `venv`)

### 1. Initialize Containers & Volumes
Start all Apache Airflow services (PostgreSQL, Redis, Scheduler, Dag Processor, Worker, and API Server) in detached mode:
```bash
docker compose up -d
```

### 2. Monitor Container Status
Verify that all 7 services are running and healthy:
```bash
docker compose ps
```

### 3. Trigger DAG via CLI (Optional)
You can trigger the pipeline directly using the Airflow CLI command inside the scheduler container:
```bash
docker compose exec airflow-scheduler airflow dags trigger api_processer
```

### 4. Stop Environment
Bring down all containers and clean up networks:
```bash
docker compose down
```

---

## 🔐 Environment Setup (`.env`)

Create a `.env` file in the root of your project workspace to define your secrets. Docker Compose will automatically load these:

```env
AIRFLOW_UID=50000
FERNET_KEY=kVhryrOyR8UFi4gOjiyC_oSoGPDcUMoyWDfB8Jmbbyw=
AIRFLOW_CONN_POSTGRES_LOCAL=postgresql://airflow:airflow@postgres:5432/airflow
```

> [!NOTE]
> Setting the connection string `AIRFLOW_CONN_POSTGRES_LOCAL` registers the `postgres_local` connection in Airflow automatically.

---

## 🧠 Key Learnings

1.  **Orchestration vs. Execution Separation**: Keeping heavy data logic in the `scripts/` directory and utilizing `dags/` purely for task mapping is the golden rule for keeping pipelines maintainable and readable.
2.  **Environment Ingestion (`AIRFLOW_CONN_*`)**: Airflow's automatic loading of connections from matching environment variables eliminates the need to configure connection parameters in the UI, enabling easy Infrastructure-as-Code setups.
3.  **Docker Volume Isolation & `PYTHONPATH`**: Mapping volumes dynamically while extending the container's `PYTHONPATH` allowed modules to be resolved on import without restructuring host directories.
