import unittest
from airflow.models import DagBag

class TestBreweryDataPipeline(unittest.TestCase):
    
    def setUp(self):
        # Load the DAG from the DAGs folder
        self.dagbag = DagBag(dag_folder='dags/')
    
    def test_dag_loaded(self):
        # Test if the DAG is loaded correctly
        dag = self.dagbag.get_dag('brewery_data_pipeline')
        self.assertIsNotNone(dag)  # Ensure the DAG is not None
        self.assertEqual(len(dag.tasks), 3)  # Check that there are 3 tasks
    
    def test_task_ids(self):
        # Check the task IDs to make sure they are correct
        dag = self.dagbag.get_dag('brewery_data_pipeline')
        task_ids = [task.task_id for task in dag.tasks]
        self.assertIn('ingest_data', task_ids)
        self.assertIn('transform_data', task_ids)
        self.assertIn('aggregate_data', task_ids)

if __name__ == '__main__':
    unittest.main()
