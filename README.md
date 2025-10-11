
# Data Pipeline Project with Airflow

## Project Overview

This project implements a robust **data pipeline** using **Apache Airflow** to automate the ingestion, processing, and prediction tasks. The pipeline is designed to handle batch data workflows, moving data from sources to destinations, and generating predictions automatically.

---

## Project Structure

```
├── README.md
├── airflow
│   ├── __init__.py
│   ├── airflow.cfg
│   ├── airflow.db
│   ├── dags
│   │   ├── ingestion_dag.py
│   │   ├── prediction_dag.py
│   │   └── source/
│   │   └── destination/
│   ├── logs/
│   └── ...
```

- `airflow/`: Main Airflow folder containing configuration, database, DAGs, and logs.
- `dags/`: Contains the DAG definitions for ingestion and prediction tasks.
- `logs/`: Stores execution logs of DAG runs.
- `source/` & `destination/`: Directories used for file movements during ingestion.

---

## Features

- **Automated Ingestion**: DAG for fetching data from source directories and moving to the processing area.
- **Batch Prediction**: DAG for generating predictions in batch mode.
- **Logging**: Detailed logs for each DAG and task execution.
- **Scheduling**: DAGs are scheduled with Airflow to run at defined intervals or manually triggered.

---

## Installation

1. **Clone the repository**:

```bash
git clone <your-repo-url>
cd <project-folder>
```

2. **Install dependencies** (Python 3.10+ recommended):

```bash
pip install apache-airflow
```

3. **Initialize Airflow**:

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
```

---

## Usage

### Start Airflow Services

```bash
# Start the webserver
airflow webserver --port 8080

# Start the scheduler in another terminal
airflow scheduler
```

Access the Airflow UI at [http://localhost:8080](http://localhost:8080) to monitor DAG runs.

### Trigger DAGs

- **Manual trigger**: From the Airflow UI, select the DAG and click **Trigger DAG**.
- **Scheduled runs**: DAGs will run automatically based on defined schedules in the DAG files.

---

## DAGs Description

### Ingestion DAG (`ingestion_dag.py`)

- Moves files from `raw_data/` to `destination/`.
- Checks for existing files before moving to avoid duplicates.
- Logs each run for traceability.

### Prediction DAG (`prediction_dag.py`)

- Loads batch data from the ingestion destination.
- Generates predictions using the trained model.
- Sends output to the specified location and logs each batch.

---

## Logs

- Logs are stored under `airflow/logs/` by DAG and task ID.
- Useful for debugging and monitoring DAG executions.
- Each task log includes attempt history and timestamp.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Commit your changes: `git commit -m "Description of changes"`.
5. Push to the branch: `git push origin feature-name`.
6. Create a Pull Request.

---

## License

This project is licensed under the **MIT License**.

