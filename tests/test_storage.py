import sys
import os
# Add the project root to the Python path to allow importing from 'utils'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
import shutil
from unittest.mock import patch
from datetime import datetime

# Import the module to allow modifying its global variables for testing
from utils import storage
# Also import the functions to be tested
from utils.storage import init_project, load_db, save_db, query_tasks

class TestStorage(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test directory and mock data."""
        self.test_dir = ".xixi_test"
        self.db_path = os.path.join(self.test_dir, "db.json")
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Override the default DB paths for the duration of the tests
        self.original_db_file = storage.DB_FILE
        storage.DB_FILE = self.db_path
        self.original_db_dir = storage.DB_DIR
        storage.DB_DIR = self.test_dir

        self.mock_db_data = {
            "project": {
                "project_name": "Test Project",
                "project_goal": "Test Goal"
            },
            "tasks": [
                {"task_id": "T1", "title": "Task 1", "status": "todo", "due_date": "2024-01-01"},
                {"task_id": "T2", "title": "Task 2", "status": "in_progress"},
                {"task_id": "T3", "title": "Task 3", "status": "done"},
                {"task_id": "T4", "title": "Task 4", "status": "todo", "due_date": "2025-12-31"}
            ]
        }

    def tearDown(self):
        """Clean up the test directory and restore original settings."""
        storage.DB_FILE = self.original_db_file
        storage.DB_DIR = self.original_db_dir
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_init_project(self):
        """Test project initialization."""
        init_project("Test Project", "Test Goal")
        self.assertTrue(os.path.exists(self.db_path))
        with open(self.db_path, 'r') as f:
            data = json.load(f)
        self.assertEqual(data["project"]["project_name"], "Test Project")
        self.assertEqual(data["project"]["project_goal"], "Test Goal")
        self.assertIn("project_id", data["project"])
        self.assertIn("created_at", data["project"])

    def test_load_and_save_db(self):
        """Test loading and saving data."""
        # Test saving
        save_db(self.mock_db_data)
        self.assertTrue(os.path.exists(self.db_path))

        # Test loading
        data = load_db()
        self.assertEqual(data, self.mock_db_data)

    @patch('utils.storage.datetime')
    @patch('utils.storage.load_db')
    def test_query_tasks(self, mock_load_db, mock_datetime):
        """Test querying tasks with different criteria."""
        mock_load_db.return_value = self.mock_db_data

        # Test querying by status
        todo_tasks = query_tasks(status=['todo'])
        self.assertEqual(len(todo_tasks), 2)
        self.assertTrue(all(t['status'] == 'todo' for t in todo_tasks))

        # Test querying for overdue tasks
        # Configure the mock to return a fixed date and keep fromisoformat functional
        mock_datetime.now.return_value.date.return_value = datetime(2024, 1, 2).date()
        mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)
        
        overdue_tasks = query_tasks(overdue=True)
        self.assertEqual(len(overdue_tasks), 1)
        self.assertEqual(overdue_tasks[0]['task_id'], 'T1')

        # Test querying with no criteria (should return all tasks)
        all_tasks = query_tasks()
        self.assertEqual(len(all_tasks), 4)

if __name__ == '__main__':
    unittest.main()
