import unittest
from pyspark.sql import SparkSession
from aggregate_data import aggregate_breweries_data
import os

class TestAggregateData(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Initialize a Spark session for testing
        cls.spark = SparkSession.builder.master("local[1]").appName("BreweryDataPipelineTest").getOrCreate()

    @classmethod
    def tearDownClass(cls):
        # Stop Spark session after tests
        cls.spark.stop()

    def test_aggregate_breweries_data(self):
        # Assuming there's already a transformed Parquet file in the Silver layer
        transformed_data_path = "data/silver/test_breweries_transformed.parquet"
        aggregated_data_path = "data/gold/test_aggregated_breweries.parquet"
        
        # Run the aggregation
        aggregate_breweries_data(self.spark, transformed_data_path, aggregated_data_path)
        
        # Verify that the aggregated Parquet file was created
        self.assertTrue(os.path.exists(aggregated_data_path))
        
        # Read the aggregated data to verify its contents
        df = self.spark.read.parquet(aggregated_data_path)
        self.assertGreater(df.count(), 0)  # Ensure that the DataFrame has data
        self.assertIn('brewery_type', df.columns)  # Ensure that 'brewery_type' is a column
        self.assertIn('location', df.columns)  # Ensure that 'location' is a column

if __name__ == '__main__':
    unittest.main()
