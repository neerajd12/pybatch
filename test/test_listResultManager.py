import unittest
from mock import patch
from pybatch.result import ListResultManager, JobSuccess, JobError


class TestListResultManager(unittest.TestCase):

    @patch('pybatch.result.ListResultManager.add_error')
    @patch('pybatch.result.ListResultManager.add_success')
    def test_add_results_success(self, add_success, add_error):
        result_manager = ListResultManager()
        result_manager.add_results(JobSuccess(1, 1))
        self.assertTrue(add_success.called)
        self.assertFalse(add_error.called)

    @patch('pybatch.result.ListResultManager.add_error')
    @patch('pybatch.result.ListResultManager.add_success')
    def test_add_results_error(self, add_success, add_error):
        result_manager = ListResultManager()
        result_manager.add_results(JobError(1, 1))
        self.assertTrue(add_error.called)
        self.assertFalse(add_success.called)

    @patch('pybatch.result.ListResultManager.add_error')
    @patch('pybatch.result.ListResultManager.add_success')
    def test_add_results_invalid_result_type(self, add_success, add_error):
        result_manager = ListResultManager()
        with self.assertRaises(TypeError) as e:
            result_manager.add_results(1)

    def test_add_success(self):
        result_manager = ListResultManager()
        result_manager.add_success(JobSuccess(1, 1))
        self.assertEqual(len(result_manager.results), 1)
        self.assertEqual(type(result_manager.results[0]).__name__, JobSuccess.__name__)
        self.assertEqual(result_manager.results[0].job_id, 1)
        self.assertEqual(result_manager.results[0].result, 1)

    def test_add_success_error_type(self):
        result_manager = ListResultManager()
        with self.assertRaises(AssertionError) as e:
            result_manager.add_success(JobError(1, 1))

    def test_add_success_invalid_type(self):
        result_manager = ListResultManager()
        with self.assertRaises(AssertionError) as e:
            result_manager.add_success(1)

    def test_add_error(self):
        result_manager = ListResultManager()
        result_manager.add_error(JobError(1, 1))
        self.assertEqual(len(result_manager.errors), 1)
        self.assertEqual(type(result_manager.errors[0]).__name__, JobError.__name__)
        self.assertEqual(result_manager.errors[0].job_id, 1)
        self.assertEqual(result_manager.errors[0].result, 1)

    def test_add_error_success_type(self):
        result_manager = ListResultManager()
        with self.assertRaises(AssertionError) as e:
            result_manager.add_error(JobSuccess(1, 1))

    def test_add_error_invalid_type(self):
        result_manager = ListResultManager()
        with self.assertRaises(AssertionError) as e:
            result_manager.add_error(1)

    def test_show_results(self):
        result_manager = ListResultManager()
        result_manager.add_success(JobSuccess(1, 1))
        result = result_manager.show_results()
        self.assertEqual(len(result), 1)
        self.assertEqual(type(result[0]).__name__, JobSuccess.__name__)
        self.assertEqual(result[0].job_id, 1)
        self.assertEqual(result[0].result, 1)
        result_manager = ListResultManager()
        result = result_manager.show_results()
        self.assertEqual(len(result), 0)

    def test_show_errors(self):
        result_manager = ListResultManager()
        result_manager.add_error(JobError(1, 1))
        result = result_manager.show_errors()
        self.assertEqual(len(result), 1)
        self.assertEqual(type(result[0]).__name__, JobError.__name__)
        self.assertEqual(result[0].job_id, 1)
        self.assertEqual(result[0].result, 1)
        result_manager = ListResultManager()
        result = result_manager.show_results()
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
