import unittest
from data_proxy import ListDataProxy


class TestListDataProxy(unittest.TestCase):

    def test_get_data_size(self):
        data_proxy = ListDataProxy([1, 2, 3, 4])
        self.assertEqual(data_proxy.get_data_size(), 4)

    def test_get_data_size_no_data(self):
        data_proxy = ListDataProxy()
        with self.assertRaises(TypeError) as e:
            data_proxy.get_data_size()


if __name__ == "__main__":
    unittest.main()
