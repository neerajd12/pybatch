import unittest
from data_proxy import ListDataProxy
from partitioner import SimpleListPartitioner


class TestSimpleListPartitioner(unittest.TestCase):

    def test_get_partition(self):
        data_proxy = ListDataProxy(data=range(100))
        partitioner = SimpleListPartitioner(processors=4, data_proxy=data_proxy)
        part_id, part = partitioner.get_partition()
        self.assertEqual(part, range(0, 25))
        part_id, part = partitioner.get_partition()
        self.assertEqual(part, range(25, 50))
        part_id, part = partitioner.get_partition()
        self.assertEqual(part, range(50, 75))
        part_id, part = partitioner.get_partition()
        self.assertEqual(part, range(75, 100))
        part_id, part = partitioner.get_partition()
        self.assertEqual(part, [])


if __name__ == "__main__":
    unittest.main()
