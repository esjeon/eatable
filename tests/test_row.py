
import unittest
from eatable import Table, Row

class RowTestCase(unittest.TestCase):
    def setUp(self):
        self.header = ('A', 'B', 'C')
        self.table = Table(self.header)

    def test_init(self):
        Row(self.table, 0, ('a1', 'b2', 'c2'))

    def test_getitem(self):
        row = Row(self.table, 0, ('a1', 'b1', 'c1'))
        self.assertEqual(row['A'], 'a1')
        self.assertEqual(row['B'], 'b1')
        self.assertEqual(row['C'], 'c1')

if __name__ == '__main__':
    unittest.main()
