import sys
import os
# Add the project root to the Python path to allow importing from 'utils'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from utils.llm_api import decompose_requirement, get_task_advice, generate_report, answer_question

class TestLlmApi(unittest.TestCase):

    def setUp(self):
        """Set up common mock data for tests."""
        self.mock_project_context = {
            "project": {"project_name": "Test Project", "project_goal": "Finish the test suite"},
            "tasks": [{"task_id": "T1", "title": "Existing Task", "status": "todo"}]
        }
        self.mock_task = {"task_id": "T1", "title": "Write a unit test", "description": "..."}

    @patch('utils.llm_api.call_llm')
    def test_decompose_requirement(self, mock_call_llm):
        """Test that decompose_requirement correctly parses valid LLM YAML output."""
        # Mock the raw YAML string returned by the LLM
        mock_llm_response = """
        ```yaml
        - task_id: "T2"
          parent_id: null
          title: "New Task 1"
          description: "First new task from requirement."
          status: "todo"
          difficulty: 2
          estimated_hours: 5
          due_date: "2024-08-01"
          dependencies: ["T1"]
          checklist:
            - item: "Sub-item 1"
              done: false
        - task_id: "T3"
          title: "New Task 2"
          description: "Second new task."
          status: "in_progress"
        ```"""
        mock_call_llm.return_value = mock_llm_response

        requirement = "Create two new tasks"
        new_tasks = decompose_requirement(requirement, self.mock_project_context)

        # Verify that call_llm was called with a prompt
        mock_call_llm.assert_called_once()
        self.assertIn(requirement, mock_call_llm.call_args[0][0]) # Check if requirement is in the prompt

        # Verify the parsed output
        self.assertIsInstance(new_tasks, list)
        self.assertEqual(len(new_tasks), 2)
        self.assertEqual(new_tasks[0]['title'], "New Task 1")
        self.assertEqual(new_tasks[1]['status'], "in_progress")
        self.assertIn("dependencies", new_tasks[0])
        self.assertEqual(new_tasks[0]['dependencies'][0], "T1")

    @patch('utils.llm_api.call_llm')
    def test_decompose_requirement_invalid_yaml(self, mock_call_llm):
        """Test that decompose_requirement returns an empty list for invalid YAML."""
        mock_call_llm.return_value = "This is not valid YAML"
        
        new_tasks = decompose_requirement("test requirement", self.mock_project_context)
        self.assertEqual(new_tasks, [])

    @patch('utils.llm_api.call_llm')
    def test_get_task_advice(self, mock_call_llm):
        """Test that get_task_advice returns the direct LLM response."""
        mock_advice = "Just do it!"
        mock_call_llm.return_value = mock_advice

        advice = get_task_advice(self.mock_task, self.mock_project_context)

        mock_call_llm.assert_called_once()
        self.assertIn(self.mock_task['title'], mock_call_llm.call_args[0][0])
        self.assertEqual(advice, mock_advice)

    @patch('utils.llm_api.call_llm')
    def test_generate_report(self, mock_call_llm):
        """Test that generate_report returns the direct LLM response."""
        mock_report = "# Project Report\nEverything is on track."
        mock_call_llm.return_value = mock_report

        report = generate_report(self.mock_project_context)

        mock_call_llm.assert_called_once()
        self.assertEqual(report, mock_report)

    @patch('utils.llm_api.call_llm')
    def test_answer_question(self, mock_call_llm):
        """Test that answer_question returns the direct LLM response."""
        mock_answer = "The answer is 42."
        mock_call_llm.return_value = mock_answer

        question = "What is the meaning of life?"
        answer = answer_question(question, self.mock_project_context)

        mock_call_llm.assert_called_once()
        self.assertIn(question, mock_call_llm.call_args[0][0])
        self.assertEqual(answer, mock_answer)

if __name__ == '__main__':
    unittest.main()
