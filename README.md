# Airflow Spark Hive MinIO Data Platform

This project provides a local data platform for running ETL pipelines using Apache Airflow, Spark, Hive, PostgreSQL, and MinIO (S3-compatible storage) via Docker Compose.

## Features

- **Airflow**: Orchestrates ETL workflows.
- **Spark**: Executes distributed data processing jobs.
- **Hive**: Provides SQL-like interface and metastore for Spark.
- **PostgreSQL**: Backs Hive Metastore and Airflow metadata.
- **MinIO**: S3-compatible object storage for data lake use cases.

---

## Directory Structure

```
.
├── .env
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── airflow/
│   ├── config/
│   ├── dags/
│   │   ├── etl_spark_hive_to_s3_dag.py
│   │   ├── __pycache__/
│   │   └── scripts/
│   │       ├── export_hive_to_s3_job.py
│   │       └── __pycache__/
│   └── plugins/
├── drivers/
│   └── postgresql.jar
├── hadoop/
│   └── core-site.xml
├── hive/
│   ├── hive-site.xml
│   └── scripts/
├── spark/
│   ├── spark-defaults.conf
│   └── warehouse/
└── spark-warehouse/
```

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Getting Started

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd airflow_data_platform_complete
```

### 2. Set Environment Variables

Edit the `.env` file if you want to change default credentials or bucket names.

### 3. Build and Start the Services

```sh
docker-compose build
docker-compose up
```

The first run may take several minutes as images are built and dependencies are installed.

---

## Airflow DAGs

- **[etl_spark_hive_to_s3_dag.py](airflow/dags/etl_spark_hive_to_s3_dag.py)**:  
  Submits a Spark job that reads from Hive and writes to MinIO S3.

- **[export_hive_to_s3_job.py](airflow/dags/scripts/export_hive_to_s3_job.py)**:  
  Spark script that creates a Hive table, inserts sample data, and exports it as CSV to MinIO.

---

## Service UI Links

| Service         | URL                                 | Notes                |
|-----------------|-------------------------------------|----------------------|
| Airflow         | [http://localhost:8082](http://localhost:8082) | Airflow web UI       |
| Spark Master    | [http://localhost:8088](http://localhost:8088) | Spark master UI      |
| Spark Worker    | [http://localhost:8081](http://localhost:8081) | Spark worker UI      |
| MinIO Console   | [http://localhost:9004](http://localhost:9004) | MinIO web UI         |

- **MinIO Credentials:**  
  - Access Key: `minioadmin` (or as set in `.env`)
  - Secret Key: `minioadmin` (or as set in `.env`)

---

## Usage

1. **Access Airflow UI:**  
   Go to [http://localhost:8082](http://localhost:8082)  
   Login with:  
   - Username: `admin`
   - Password: `admin`

2. **Trigger the DAG:**  
   - Enable and trigger the `etl_spark_hive_to_s3` DAG.

3. **Monitor Spark Jobs:**  
   - Spark Master UI: [http://localhost:8088](http://localhost:8088)
   - Spark Worker UI: [http://localhost:8081](http://localhost:8081)

4. **Check Output in MinIO:**  
   - Go to [http://localhost:9004](http://localhost:9004)
   - Login with MinIO credentials.
   - Browse to the bucket (default: `my-bucket`) and check the output folder.

---

## Customization

- **Add new DAGs:** Place Python files in `airflow/dags/`.
- **Add new Spark jobs:** Place scripts in `airflow/dags/scripts/`.
- **Configure Hive/Spark:** Edit `hive/hive-site.xml` and `spark/spark-defaults.conf`.
- **Add JDBC drivers:** Place `.jar` files in `drivers/`.

---

## Stopping and Cleaning Up

To stop the services:

```sh
docker-compose down
```

To remove all data (including PostgreSQL and MinIO volumes):

```sh
docker-compose down -v
```

---

## Troubleshooting

- If you change `requirements.txt` or the Dockerfile, rebuild the images:
  ```sh
  docker-compose build
  ```
- Ensure all ports required by the services are free.
- Check logs using:
  ```sh
  docker-compose logs -f
  ```

---

## License

MIT License. See [LICENSE](LICENSE) for