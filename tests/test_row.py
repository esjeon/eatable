
import unittest
from eatable import Table, Row

class RowTestCase(unittest.TestCase):
    def setUp(self):
        self.header = ('A', 'B', 'C')
        self.table = Table(self.header)
        self.table.append(('a1', 'b1', 'c1'))
        self.table.append(('a2', 'b2', 'c2'))

    def test_init(self):
        Row(self.table, 0)

    def test_getitem(self):
        row = Row(self.table, 0)
        self.assertEqual(row[0], 'a1')
        self.assertEqual(row[1], 'b1')
        self.assertEqual(row[2], 'c1')

    def test_iter(self):
        row = Row(self.table, 0)
        row_iter = iter(row)
        self.assertEqual(next(row_iter), ('A', 'a1'))
        self.assertEqual(next(row_iter), ('B', 'b1'))
        self.assertEqual(next(row_iter), ('C', 'c1'))

    def test_setitem(self):
        row = Row(self.table, 0)
        row[0] = '_1'
        self.assertEqual(row[0], '_1')
        row[0] = 'a1'
        self.assertEqual(row[0], 'a1')

    def test_select(self):
        row = Row(self.table, 0)
        self.assertEqual(row.select('A'), ('a1',))
        self.assertEqual(row.select('B', 'C'), ('b1', 'c1'))

    def test_update(self):
        row = Row(self.table, 0)
        row.update(values=('a3', 'b3', 'c3'))
        self.assertEqual(row[0], 'a3')
        self.assertEqual(row[1], 'b3')
        self.assertEqual(row[2], 'c3')

        row.update(columns=(0,1,2), values=('a1', 'b1', 'c1'))
        self.assertEqual(row[0], 'a1')
        self.assertEqual(row[1], 'b1')
        self.assertEqual(row[2], 'c1')

        with self.assertRaises(TypeError) as cm:
            row.update()

if __name__ == '__main__':
    unittest.main()
