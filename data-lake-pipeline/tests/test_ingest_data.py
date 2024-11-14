import unittest
from ingest_data import ingest_breweries

class TestIngestData(unittest.TestCase):
    
    def test_ingest_breweries(self):
        # Test to check if the data ingestion works correctly.
        data = ingest_breweries()
        # Ensure the data is a list
        self.assertIsInstance(data, list)
        # Ensure each item in the list is a dictionary
        self.assertTrue(all(isinstance(item, dict) for item in data))
        # Check if some required keys are present in the first brewery data
        if data:
            self.assertIn('name', data[0])
            self.assertIn('brewery_type', data[0])

if __name__ == '__main__':
    unittest.main()
