import unittest
from pyspark.sql import SparkSession
from transform_data import transform_breweries
from ingest_data import ingest_breweries
import os

class TestTransformData(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Initialize a Spark session for testing
        cls.spark = SparkSession.builder.master("local[1]").appName("BreweryDataPipelineTest").getOrCreate()

    @classmethod
    def tearDownClass(cls):
        # Stop Spark session after tests
        cls.spark.stop()

    def test_transform_breweries(self):
        # Test the transformation of raw brewery data into structured data
        raw_data = ingest_breweries()
        transformed_data_path = "data/silver/test_breweries_transformed.parquet"
        
        # Run the transformation
        transform_breweries(self.spark, raw_data, transformed_data_path)
        
        # Verify that the Parquet file was created
        self.assertTrue(os.path.exists(transformed_data_path))
        
        # Read the Parquet file to verify its contents
        df = self.spark.read.parquet(transformed_data_path)
        self.assertGreater(df.count(), 0)  # Ensure that the DataFrame has data

    def test_invalid_data_format(self):
        # Test for invalid data handling (assuming you provide faulty data)
        invalid_data = "invalid data"
        with self.assertRaises(TypeError):
            transform_breweries(self.spark, invalid_data, "data/silver/invalid_output.parquet")

if __name__ == '__main__':
    unittest.main()
