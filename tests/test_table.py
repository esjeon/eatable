
import unittest
from eatable import Table, Row

class TableTestCase(unittest.TestCase):
    """Test the methods of Table"""

    def setUp(self):
        self.header = ['A', 'B', 'C']
        self.length = 3
        self.table = Table(self.header)
        for i in range(self.length):
            self.table.append(('a' + str(i), 'b' + str(i), 'c' + str(i)))

    def test_from_csv_file(self):
        table = Table.from_csv_file("tests/simple.csv")
        self.assertEqual(len(table), 3)

    def test_init_append(self):
        self.assertEqual(self.table.width, len(self.header))
        self.assertEqual(self.table.data[0], ('a0', 'b0', 'c0'))
        self.assertEqual(self.table.data[1], ('a1', 'b1', 'c1'))
        self.assertEqual(self.table.data[2], ('a2', 'b2', 'c2'))

    def test_getitem(self):
        row = self.table[0]
        self.assertIsInstance(row, Row)

    def test_iter(self):
        for row, i in zip(self.table, range(self.length)):
            data = ('a' + str(i), 'b' + str(i), 'c' + str(i))
            self.assertEqual(row.get_data(), data)

    def test_setitem(self):
        self.table[0] = ('x1', 'y1', 'z1')
        self.assertEqual(self.table.data[0], ('x1', 'y1', 'z1'))

    def test_append(self):
        # normal case is already tested
        with self.assertRaises(AssertionError):
            self.table.append((1, 2, 3, 4))

    def test_get_row(self):
        row = self.table.get_row(0)
        self.assertIsInstance(row, Row)
        self.assertEqual(row.table, self.table)
        self.assertEqual(row.index, 0)

        with self.assertRaises(IndexError):
            self.table.get_row(30)

    def test_set_row(self):
        self.table.set_row(0, range(3))
        self.assertEqual(self.table.data[0], tuple(range(3)))

        with self.assertRaises(IndexError):
            self.table.set_row(30, range(3))


    def test_get_column_index(self):
        self.assertEqual(self.table.get_column_index('A'), 0)
        self.assertEqual(self.table.get_column_index('B'), 1)
        self.assertEqual(self.table.get_column_index('C'), 2)
        self.assertEqual(self.table.get_column_index(0), 0)
        self.assertEqual(self.table.get_column_index(1), 1)
        self.assertEqual(self.table.get_column_index(2), 2)

        with self.assertRaises(IndexError):
            self.table.get_column_index(10)
        with self.assertRaises(KeyError):
            self.table.get_column_index('D')
        with self.assertRaises(TypeError):
            self.table.get_column_index(['E'])

    def test_update(self):
        self.table.update(
            ('A', 'B'),
            {
                0: ('00', '11')
            }
        )
        self.assertEqual(self.table.get_row_data(0), ('00', '11', 'c0'))


if __name__ == '__main__':
    unittest.main()
