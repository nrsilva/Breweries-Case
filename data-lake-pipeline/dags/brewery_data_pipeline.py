from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from ingest_data import ingest_breweries
from transform_data import transform_breweries
from aggregate_data import aggregate_breweries_data
from utils import create_dir_if_not_exists
from pyspark.sql import SparkSession

# Function to initialize the Spark session
def init_spark():
    """
    Initialize a Spark session for processing data in PySpark.
    :return: Spark session object
    """
    spark = SparkSession.builder \
        .appName("Brewery Data Pipeline") \
        .config("spark.sql.warehouse.dir", "file:///C:/tmp") \
        .getOrCreate()
    return spark

# Function to ingest data from the Open Brewery DB API
def ingest_data_task():
    """
    Task to ingest brewery data from the Open Brewery DB API.
    :return: Raw brewery data in JSON format
    """
    print("Ingesting brewery data from the Open Brewery DB API...")
    raw_data = ingest_breweries()  # This function is defined in the ingest_data.py
    return raw_data

# Function to transform the raw data and save it to the Silver layer
def transform_data_task(raw_data):
    """
    Task to transform the raw brewery data into a structured format and save it in the Silver layer.
    :param raw_data: Raw brewery data (in JSON format)
    """
    spark = init_spark()
    
    # Creating directories for Silver and Gold layers if they don't exist
    create_dir_if_not_exists("data/silver")
    transformed_data_path = "data/silver/breweries_transformed.parquet"
    
    print("Transforming raw data and saving to Silver layer...")
    transform_breweries(spark, raw_data, transformed_data_path)

# Function to aggregate the transformed data and save it to the Gold layer
def aggregate_data_task():
    """
    Task to aggregate the brewery data (count breweries by type and location) and save it in the Gold layer.
    """
    spark = init_spark()
    
    # Creating directories for Gold layer if they don't exist
    create_dir_if_not_exists("data/gold")
    transformed_data_path = "data/silver/breweries_transformed.parquet"
    aggregated_data_path = "data/gold/aggregated_breweries.parquet"
    
    print("Aggregating transformed data and saving to Gold layer...")
    aggregate_breweries_data(spark, transformed_data_path, aggregated_data_path)

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}

# Define the DAG
with DAG(
    'brewery_data_pipeline',
    default_args=default_args,
    description='A data pipeline to ingest, transform, and aggregate brewery data',
    schedule_interval='@daily',  # Run the pipeline daily
    start_date=days_ago(1),  # Start the pipeline one day ago
    tags=['brewery', 'data-pipeline'],
) as dag:
    
    # Task 1: Ingest Data from Open Brewery DB API
    ingest_data = PythonOperator(
        task_id='ingest_data',
        python_callable=ingest_data_task,
    )
    
    # Task 2: Transform Raw Data and Save to Silver Layer
    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data_task,
        op_args=['{{ task_instance.xcom_pull(task_ids="ingest_data") }}'],
    )
    
    # Task 3: Aggregate Data and Save to Gold Layer
    aggregate_data = PythonOperator(
        task_id='aggregate_data',
        python_callable=aggregate_data_task,
    )

    # Set the task dependencies
    ingest_data >> transform_data >> aggregate_data
