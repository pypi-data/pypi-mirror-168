import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from time import time

from src.test_kata_anagrams_weabreu.anagrams import search_anagrams_v7, AnagramsAnalyzer

# class AnagramsTest(unittest.TestCase):
#     def setUp(self) -> None:
#         super(AnagramsTest, self).setUp()
#         self.input_data = [
#             "crepitus", "piecrust", "spate", "tapes", "tepas", 
#             "punctilio", "unpolitic", "paste", "pates", "peats", "pepta", 
#             "sunders", "undress", "cuprites", "pictures", "sort", "a"
#         ]
#         self.expected_data = (
#             ["crepitus piecrust cuprites pictures", 
#             "spate tapes tepas paste pates peats", 
#             "punctilio unpolitic", "sunders undress"],
#             14,
#             "punctilio unpolitic",
#             "spate tapes tepas paste pates peats"
#         )

#     def test_should_execute_in_less_than_1_8s(self):
#         start_time = time()
#         search_anagrams_v7(self.input_data)
#         stop_time = time()

#         self.assertTrue((stop_time - start_time) < 1.8)

#     def test_should_return_expected_values(self):
#         result = search_anagrams_v7(self.input_data)
#         self.assertEqual(result, self.expected_data)
    
#     def test_should_return_empty_list_if_does_not_contains_anagrams(self):
#         result = search_anagrams_v7(["sort", "a"])
#         self.assertEqual(result, ([], 0, "", ""))

class AnagramsAnalyzerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.input_data = [
            "crepitus", "piecrust", "spate", "tapes", "tepas", 
            "punctilio", "unpolitic", "paste", "pates", "peats", "pepta", 
            "sunders", "undress", "cuprites", "pictures", "sort", "a"
        ]
        self.expected_result =  [
            "crepitus piecrust cuprites pictures", 
            "spate tapes tepas paste pates peats", 
            "punctilio unpolitic", "sunders undress"
        ]
        return super().setUp()

    def test_get_anagrams_should_return_a_list_of_anagrams(self):
        analyzer = AnagramsAnalyzer(self.input_data)
        self.assertEqual(analyzer.get_anagrams(), self.expected_result)

    def test_get_anagrams_should_return_an_empty_list_if_input_does_not_contains_anagrams(self):
        analyzer = AnagramsAnalyzer(["sort", "a"])
        self.assertEqual(analyzer.get_anagrams(), [])

if __name__ == "__main__":
    unittest.main()
