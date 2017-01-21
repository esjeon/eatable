
import unittest
from eatable import Table

class UseCaseTestCase(unittest.TestCase):
    """Test some practical usecases"""
    def setUp(self):
        self.people = Table.from_csv_file("tests/people.csv")

    def test_people_by_city(self):
        result = self.people.select('name', where=lambda row:(
            row['city'] == 'Waterloo'
        ))
        self.assertEqual(result.width, 1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Jack')
        self.assertEqual(result[1]['name'], 'Frank')

        lst = result.to_list(flatten=True)
        self.assertEqual(lst, ['Jack', 'Frank'])

if __name__ == '__main__':
    unittest.main()
