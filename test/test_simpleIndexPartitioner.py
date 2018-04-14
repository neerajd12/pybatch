import unittest
from data_proxy import ListDataProxy
from partitioner import SimpleIndexPartitioner


class TestSimpleIndexPartitioner(unittest.TestCase):

    def test_init_no_data_proxy(self):
        with self.assertRaises(AssertionError) as e:
            SimpleIndexPartitioner()

    def test_init_invalid_data_proxy(self):
        with self.assertRaises(AssertionError) as e:
            SimpleIndexPartitioner(data_proxy=[])

    def test_init(self):
        data_proxy = ListDataProxy(data=range(100))
        partitioner = SimpleIndexPartitioner(processors=4, data_proxy=data_proxy)
        self.assertEqual(partitioner.start_index, 0)
        self.assertEqual(partitioner.end_index, 0)
        self.assertEqual(partitioner.data_size, 100)
        self.assertEqual(partitioner.batch_size, 25)
        self.assertEqual(partitioner.processors, 4)

    def test_update_indexes(self):
        data_proxy = ListDataProxy(data=range(100))
        partitioner = SimpleIndexPartitioner(processors=4, data_proxy=data_proxy)
        for i in range(partitioner.processors):
            pt = partitioner.update_indexes()
            self.assertEqual(pt, i*partitioner.batch_size)
            self.assertEqual(partitioner.start_index, (i+1)*partitioner.batch_size)
            self.assertEqual(partitioner.end_index, (i+1)*partitioner.batch_size)
            self.assertEqual(partitioner.partitions, i+1)

    def test_update_indexes_non_zero_start(self):
        data_proxy = ListDataProxy(data=range(100))
        partitioner = SimpleIndexPartitioner(processors=4, data_proxy=data_proxy, start_index=10)
        for i in range(partitioner.processors-1):
            pt = partitioner.update_indexes()
            self.assertEqual(pt, (i*partitioner.batch_size)+10)
            self.assertEqual(partitioner.start_index, (i+1)*partitioner.batch_size+10)
            self.assertEqual(partitioner.end_index, (i+1)*partitioner.batch_size+10)
            self.assertEqual(partitioner.partitions, i+1)
        pt = partitioner.update_indexes()
        self.assertEqual(pt, 85)
        self.assertEqual(partitioner.start_index, 100)
        self.assertEqual(partitioner.end_index, 100)
        self.assertEqual(partitioner.partitions, 4)

    def test_get_partition(self):
        data_proxy = ListDataProxy(data=range(100))
        partitioner = SimpleIndexPartitioner(processors=4, data_proxy=data_proxy)
        for i in range(partitioner.processors):
            part_id, pt_start, pt_end = partitioner.get_partition()
            self.assertEqual(pt_start, i * partitioner.batch_size)
            self.assertEqual(pt_end, (i + 1) * partitioner.batch_size)
        part_id, pt_start, pt_end = partitioner.get_partition()
        self.assertEqual(pt_start, -1)
        self.assertEqual(pt_end, -1)


if __name__ == "__main__":
    unittest.main()
