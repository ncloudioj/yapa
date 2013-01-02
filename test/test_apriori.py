

import unittest
from yapa import apriori

universal_sets = range(6)
data_sets = [set([0, 1, 2]),
             set([3, 4, 5]),
             set([0, 3]),
             set([0, 1, 3, 4]),
             set([0, 1, 2, 3]),
             set([0, 2]),
             set([1, 3, 4]),
             set([0, 1, 3, 4, 5])]

class TestNaiveApriori(unittest.TestCase):

    def setUp(self):
        self.ap = apriori.NaiveApriori(universal_sets, support_criterion=0.5)
        self.ap.generate_rules(data_sets)

    def test_frequent_rules_cardinality_1(self):
        frequent_sets = self.ap.get_frequent_sets(1)
        self.assertEqual(frequent_sets,
                         {(0,):6,
                          (1,):5,
                          (3,):6,
                          (4,):4})

    def test_frequent_rules_cardinality_2(self):
        frequent_sets = self.ap.get_frequent_sets(2)
        self.assertEqual(frequent_sets,
                         {(0, 1):4,
                          (0, 3):4,
                          (3, 4):4,
                          (1, 3):4})


    def test_frequent_rules_cardinality_3(self):
        frequent_sets = self.ap.get_frequent_sets(3)
        self.assertEqual(frequent_sets,
                         {})
