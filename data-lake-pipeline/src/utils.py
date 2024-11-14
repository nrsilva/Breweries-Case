import os
import datetime
from pyspark.sql import SparkSession

# Function to initialize a Spark session
def init_spark(app_name="DataLakePipeline", master="local[4]"):
    """
    Initializes and returns a Spark session.
    
    :param app_name: Name of the Spark application (default: "DataLakePipeline")
    :param master: Spark master configuration (default: "local[4]")
    :return: Configured SparkSession
    """
    # Create a Spark session with the given configuration
    spark = SparkSession.builder \
        .appName(app_name) \
        .master(master) \
        .getOrCreate()
    
    # Log the Spark version (optional)
    print(f"Spark session started with version: {spark.version}")
    return spark

# Function to generate a unique filename based on the current timestamp
def generate_unique_filename(prefix="file", extension="parquet"):
    """
    Generates a unique filename using the current timestamp.
    
    :param prefix: Prefix for the filename (default: "file")
    :param extension: File extension (default: "parquet")
    :return: Unique filename with timestamp
    """
    # Get the current timestamp in the format YYYY-MM-DD_HH-MM-SS
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Generate the filename with the prefix, timestamp, and extension
    return f"{prefix}_{timestamp}.{extension}"

# Function to save a DataFrame as a Parquet file
def save_parquet(df, path, mode="overwrite"):
    """
    Saves a DataFrame as a Parquet file.
    
    :param df: DataFrame to be saved
    :param path: Path where the Parquet file will be saved
    :param mode: Write mode (default: "overwrite")
    """
    # Write the DataFrame to the specified path in Parquet format
    df.write.mode(mode).parquet(path)
    
    # Log the saved file path (optional)
    print(f"Data saved to: {path}")

# Function to read a Parquet file into a DataFrame
def read_parquet(spark, path):
    """
    Reads a Parquet file and returns a DataFrame.
    
    :param spark: SparkSession instance
    :param path: Path to the Parquet file
    :return: DataFrame containing the data from the Parquet file
    """
    # Read the Parquet file and return it as a DataFrame
    return spark.read.parquet(path)

# Function to ensure a directory exists; if it doesn't, create it
def create_dir_if_not_exists(directory):
    """
    Creates a directory if it doesn't exist.
    
    :param directory: Path to the directory
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        # Create the directory if it doesn't exist
        os.makedirs(directory)
        print(f"Directory created: {directory}")
    else:
        # Log that the directory already exists (optional)
        print(f"Directory already exists: {directory}")
