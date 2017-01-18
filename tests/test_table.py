
import unittest
from eatable import Table

class TableTestCase(unittest.TestCase):
    """Test the methods of Table"""

    def setUp(self):
        self.header = ['A', 'B', 'C']

    def test_init(self):
        table = Table(self.header)
        self.assertEqual(table.width, len(self.header))

    def test_get_column_index(self):
        table = Table(self.header)
        self.assertEqual(table.get_column_index('A'), 0)
        self.assertEqual(table.get_column_index('B'), 1)
        self.assertEqual(table.get_column_index('C'), 2)

    def test_append(self):
        table = Table(self.header)
        for i in range(5):
            table.append(('a' + str(i), 'b' + str(i), 'c' + str(i)))

        self.assertEqual(len(table.data), 5)
        for i in range(5):
            self.assertIsInstance(table.data[i], tuple)

if __name__ == '__main__':
    unittest.main()