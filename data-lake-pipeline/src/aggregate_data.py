from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

# Import utility functions
from utils import read_parquet, save_parquet

def aggregate_breweries_data(spark, input_path, output_path):
    """
    Aggregate brewery data based on the brewery type and location.
    The aggregation will count the number of breweries by type and location.
    
    :param spark: Spark session object
    :param input_path: Path to the input Parquet file (transformed data from the silver layer)
    :param output_path: Path to save the aggregated data in the gold layer (output Parquet file)
    """
    # Step 1: Load the transformed data (silver layer) from the specified input path
    df = read_parquet(spark, input_path)
    
    # Step 2: Perform aggregation: Count breweries by type and location
    # Group by 'brewery_type' and 'city', and count the number of breweries in each group
    aggregated_df = df.groupBy("brewery_type", "city").agg(count("id").alias("brewery_count"))
    
    # Step 3: Save the aggregated result as a Parquet file in the gold layer (output path)
    save_parquet(aggregated_df, output_path)

    # Optional: Print some results for debugging purposes
    aggregated_df.show(10)

if __name__ == "__main__":
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("Aggregate Breweries Data") \
        .getOrCreate()

    # Define input and output paths
    input_parquet_path = "data/silver/breweries_transformed.parquet"  # Path to silver layer
    output_parquet_path = "data/gold/aggregated_breweries.parquet"    # Path to gold layer

    # Perform aggregation
    aggregate_breweries_data(spark, input_parquet_path, output_parquet_path)
