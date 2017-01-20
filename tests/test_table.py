
import unittest
from eatable import Table, Row

class TableTestCase(unittest.TestCase):
    """Test the methods of Table"""

    def setUp(self):
        self.header = ['A', 'B', 'C']

    def test_from_csv_file(self):
        table = Table.from_csv_file("tests/simple.csv")
        self.assertEqual(len(table), 3)

    def test_init(self):
        table = Table(self.header)
        self.assertEqual(table.width, len(self.header))

    def test_getitem(self):
        table = Table(self.header)
        table.append(('a', 'b', 'c'))
        row = table[0]
        self.assertIsInstance(row, Row)

    def test_setitem(self):
        new_data = ('a2', 'b2', 'c2')
        table = Table(self.header)
        table.append(('a1', 'b1', 'c1'))
        table[0] = new_data
        self.assertEqual(table.data[0], new_data)

    def test_get_column_index(self):
        table = Table(self.header)
        self.assertEqual(table.get_column_index('A'), 0)
        self.assertEqual(table.get_column_index('B'), 1)
        self.assertEqual(table.get_column_index('C'), 2)
        self.assertEqual(table.get_column_index(0), 0)
        self.assertEqual(table.get_column_index(1), 1)
        self.assertEqual(table.get_column_index(2), 2)

        with self.assertRaises(IndexError):
            table.get_column_index(10)
        with self.assertRaises(KeyError):
            table.get_column_index('D')
        with self.assertRaises(TypeError):
            table.get_column_index(['E'])

    def test_append(self):
        table = Table(self.header)
        for i in range(5):
            table.append(('a' + str(i), 'b' + str(i), 'c' + str(i)))

        self.assertEqual(len(table), 5)
        for i in range(5):
            self.assertIsInstance(table.data[i], tuple)

if __name__ == '__main__':
    unittest.main()
