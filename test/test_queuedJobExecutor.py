import unittest
from multiprocessing import Queue
from pybatch.executor import QueuedJobExecutor, DEFAULT_PARTITION_KEY
from pybatch.partitioner import SimpleListPartitioner
from pybatch.result import ListResultManager, JobSuccess, JobError
from pybatch.data_proxy import ListDataProxy


def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    return [i for i in data]


class TestQueuedJobExecutor(unittest.TestCase):

    def test_init(self):
        Data = ListDataProxy([i for i in range(100)])
        executor = QueuedJobExecutor(worker=test_worker,
                                     data_partitioner=SimpleListPartitioner(data_proxy=Data, processors=4),
                                     result_manager=ListResultManager())
        self.assertEqual(executor.processors, 4)
        self.assertEqual(type(executor.response), tuple)
        aa = executor.response[0]
        print(type(aa))
        self.assertTrue(type(aa).__name__, Queue.__name__)

    def test_init_invalid_partitioner(self):
        Data = ListDataProxy([i for i in range(100)])
        with self.assertRaises(AssertionError) as e:
            QueuedJobExecutor(worker=test_worker,
                              data_partitioner=Data,
                              result_manager=ListResultManager())

    def test_init_invalid_result_manager(self):
        Data = ListDataProxy([i for i in range(100)])
        with self.assertRaises(AssertionError) as e:
            QueuedJobExecutor(worker=test_worker,
                              data_partitioner=SimpleListPartitioner(data_proxy=Data, processors=4),
                              result_manager=Data)

    def test_execute(self):
        Data = ListDataProxy([i for i in range(100)])
        result = QueuedJobExecutor(worker=test_worker,
                                   data_partitioner=SimpleListPartitioner(data_proxy=Data, processors=4),
                                   result_manager=ListResultManager()).execute()
        result.show_results()
        self.assertEqual(len(result.show_results()), 4)
        self.assertEqual(len(result.show_results()[0].result), 25)
        self.assertEqual(len(result.show_results()[1].result), 25)
        self.assertEqual(len(result.show_results()[2].result), 25)
        self.assertEqual(len(result.show_results()[3].result), 25)


if __name__ == "__main__":
    unittest.main()
