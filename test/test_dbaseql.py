import unittest
import sys
sys.path.append('../')
from dbaseql.table_builder import *

class Test(unittest.TestCase):
    def setUp(self):
        url1 = "http://www.brooksbaseball.net/tabs.php?player=456034&var=so"
        url2 = "http://www.brooksbaseball.net/tabs.php?player=456034&var=po"
        self.table1 = TableBuilder.build_table(url1)
        self.table2 = TableBuilder.build_table(url2)

    def test_where(self):
        query_result = self.table1.where(lambda row: row["Pitch Type"] == "Change").select(keep_columns=["Pitch Type"])
        results = query_result.get_rows
        pitches = {pitch for result in results for (_,pitch) in result.items()}
        changeup_exists = 'Change' in pitches
        self.assertTrue(changeup_exists)

    def test_limit(self):
        query_result = self.table1.select().select(keep_columns=["Pitch Type"]).limit(2)
        results = query_result.get_rows
        num_limit = len(results)
        self.assertEqual(num_limit, 2)

    def test_join(self):
        cols = ['Pitch Type', 'Count', 'Foul/Swing', 'Whiff/Swing', 'GB/BIP', 'LD/BIP', 'FB/BIP', 'PU/BIP', 'GB/FB', \
                'HR/(FB+LD)', 'Ball', 'Strike', 'Swing', 'Foul', 'Whiffs', 'BIP', 'GB', 'LD', 'FB', 'PU', 'HR']
        joined = self.table1.join(self.table2)
        columns_joined = all(col in cols for col in joined.get_columns)
        self.assertTrue(columns_joined)


if __name__ == '__main__':
    unittest.main()