"""
Spark job to create a Hive table, insert data, and export it as CSV to MinIO S3.
"""

from pyspark.sql import SparkSession

DB_NAME = "demo_db"
TABLE_NAME = "sample_table"
S3_PATH = "s3a://my-bucket/output/demo_data"

def main():
    """
    Main function to export data from a Hive table to an S3 bucket using Apache Spark.

    This function performs the following steps:
    1. Initializes a SparkSession with Hive support enabled.
    2. Creates the target Hive database if it does not exist.
    3. Drops the target Hive table if it already exists.
    4. Creates a new Hive table with specified schema and stores it as Parquet.
    5. Inserts sample data into the Hive table.
    6. Reads the data from the Hive table into a Spark DataFrame and displays it.
    7. Writes the DataFrame to the specified S3 path in CSV format with headers.
    8. Handles exceptions by printing error messages.
    9. Ensures the SparkSession is stopped after execution.

    Comments are included throughout the function for documentation and readability.
    """
    print("Starting SparkSession...")
    spark = SparkSession.builder \
        .appName("ExportHiveToS3Job") \
        .enableHiveSupport() \
        .getOrCreate()
    print("SparkSession started.")

    try:
        print(f"Creating database {DB_NAME} if not exists...")
        spark.sql(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Dropping table {DB_NAME}.{TABLE_NAME} if exists...")
        spark.sql(f"DROP TABLE IF EXISTS {DB_NAME}.{TABLE_NAME}")
        print(f"Creating table {DB_NAME}.{TABLE_NAME}...")
        spark.sql(f"""
            CREATE TABLE {DB_NAME}.{TABLE_NAME} (id INT, name STRING) STORED AS PARQUET
        """)
        print(f"Inserting sample data into {DB_NAME}.{TABLE_NAME}...")
        spark.sql(f"""
            INSERT INTO {DB_NAME}.{TABLE_NAME} VALUES (1, 'Alice'), (2, 'Bob')
        """)

        print(f"Reading data from {DB_NAME}.{TABLE_NAME} into DataFrame...")
        df = spark.table(f"{DB_NAME}.{TABLE_NAME}")
        print("DataFrame loaded. Showing data:")
        df.show()

        print(f"Writing DataFrame to S3 path: {S3_PATH} as CSV...")
        df.write \
            .mode("overwrite") \
            .option("header", "true") \
            .csv(S3_PATH)
        print("Write to S3 completed.")
    except Exception as e:
        print(f"Error during Spark job: {e}")
    finally:
        print("Stopping SparkSession...")
        spark.stop()
        print("SparkSession stopped.")

if __name__ == "__main__":
    main()
