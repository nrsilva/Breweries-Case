from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
import json
from datetime import datetime

# Define paths
RAW_DATA_DIR = os.path.join(os.getcwd(), 'data', 'raw')
SILVER_DATA_DIR = os.path.join(os.getcwd(), 'data', 'silver')

# Initialize Spark session
spark = SparkSession.builder \
    .appName("BreweryDataTransformation") \
    .getOrCreate()

# Function to ensure the silver data directory exists
def ensure_silver_data_dir():
    if not os.path.exists(SILVER_DATA_DIR):
        os.makedirs(SILVER_DATA_DIR)

# Function to load raw data from JSON
def load_raw_data(file_path: str):
    """
    Function to load raw brewery data from a JSON file.

    Args:
        file_path (str): Path to the raw JSON file.

    Returns:
        DataFrame: Spark DataFrame containing the raw brewery data.
    """
    return spark.read.json(file_path)

# Function to transform the raw data
def transform_data(df):
    """
    Transform the raw brewery data into the desired format:
    - Select relevant columns
    - Partition by location (city or state)

    Args:
        df (DataFrame): Raw Spark DataFrame containing the brewery data.

    Returns:
        DataFrame: Transformed DataFrame ready for saving in the silver layer.
    """
    # Select relevant columns (e.g., name, type, city, state)
    df_transformed = df.select(
        "id", 
        "name", 
        "brewery_type", 
        "city", 
        "state", 
        "country"
    )

    # Handle missing or null values (optional, depending on the data quality)
    df_transformed = df_transformed.dropna(subset=["name", "brewery_type", "city", "state"])

    # You can add more transformations as needed, e.g., filtering, cleaning, etc.

    return df_transformed

# Function to save transformed data as Parquet
def save_data_as_parquet(df, filename: str):
    """
    Save the transformed brewery data as a Parquet file in the silver layer,
    partitioned by city and state.

    Args:
        df (DataFrame): Transformed Spark DataFrame.
        filename (str): The name of the Parquet file.
    """
    # Define file path for Parquet storage
    parquet_path = os.path.join(SILVER_DATA_DIR, filename)

    # Save the DataFrame as a Parquet file, partitioned by city and state
    df.write.partitionBy("city", "state").mode("overwrite").parquet(parquet_path)

    print(f"Transformed data saved as Parquet at {parquet_path}")

# Main function to perform the transformation
def transform_data_pipeline():
    # Ensure the silver data directory exists
    ensure_silver_data_dir()

    # Example: List raw files in the raw directory (you can adjust this based on your file naming convention)
    raw_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.json')]

    # Iterate over each raw file and process it
    for raw_file in raw_files:
        raw_file_path = os.path.join(RAW_DATA_DIR, raw_file)

        # Load the raw data from JSON file
        print(f"Loading raw data from {raw_file_path}...")
        raw_df = load_raw_data(raw_file_path)

        # Transform the raw data
        transformed_df = transform_data(raw_df)

        # Generate the Parquet file name based on the original file name and timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"breweries_transformed_{timestamp}.parquet"

        # Save the transformed data to Parquet
        save_data_as_parquet(transformed_df, filename)

# Execute the transformation pipeline
if __name__ == "__main__":
    transform_data_pipeline()