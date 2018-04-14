import unittest
from multiprocessing import Pipe
from executor import PipedJobExecutor, DEFAULT_PARTITION_KEY
from partitioner import SimpleListPartitioner
from result import ListResultManager, JobSuccess, JobError
from data_proxy import ListDataProxy


def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    return [i for i in data]


class TestPipedJobExecutor(unittest.TestCase):

    def test_init(self):
        Data = ListDataProxy([i for i in range(100)])
        executor = PipedJobExecutor(worker=test_worker,
                                    data_partitioner=SimpleListPartitioner(data_proxy=Data, processors=4),
                                    result_manager=ListResultManager())
        self.assertEqual(executor.processors, 4)
        aa = executor.response_holder()
        self.assertTrue(type(aa).__name__, tuple.__name__)
        self.assertTrue(type(aa[0]).__name__, Pipe.__name__)
        self.assertTrue(type(aa[1]).__name__, Pipe.__name__)

    def test_init_invalid_partitioner(self):
        Data = ListDataProxy([i for i in range(100)])
        with self.assertRaises(AssertionError) as e:
            PipedJobExecutor(worker=test_worker,
                             data_partitioner=Data,
                             result_manager=ListResultManager())

    def test_init_invalid_result_manager(self):
        Data = ListDataProxy([i for i in range(100)])
        with self.assertRaises(AssertionError) as e:
            PipedJobExecutor(worker=test_worker,
                             data_partitioner=SimpleListPartitioner(data_proxy=Data, processors=4),
                             result_manager=Data)

    def test_execute(self):
        Data = ListDataProxy([i for i in range(100)])
        result = PipedJobExecutor(worker=test_worker,
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
