import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from unittest import TestCase, main
from time import time
from src.kata_anagrams_weabreu.anagrams import search_anagrams, search_anagrams_advanced

input_data = [
    "crepitus", "piecrust", "spate", "tapes", "tepas", "punctilio", 
    "unpolitic", "paste", "pates", "peats", "septa", "sunders", "undress", 
    "cuprites", "pictures", "sort", "a"
]
input_data_all_anagrams = [
    "kinship", "pinkish", "enlist", "inlets", "listen", "silent", 
    "boaster", "boaters", "borates", "fresher", "refresh", "sinks", 
    "skins", "knits", "stink", "rots", "sort"
]

expected_data = [
    "crepitus piecrust cuprites pictures",
    "spate tapes tepas paste pates peats septa",
    "punctilio unpolitic", "sunders undress"
]
expected_data_all_anagrams = [
    "kinship pinkish", "enlist inlets listen silent", 
    "boaster boaters borates", "fresher refresh", 
    "sinks skins", "knits stink", "rots sort"
]

class TestSearchAnagrams(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_should_return_expected_data(self):
        result = search_anagrams( input_data )
        self.assertEqual(result, (expected_data, 15))

    def test_should_return_empty_list_and_0_if_receive_empty_list(self):
        result = search_anagrams([])
        self.assertEqual(result, ([], 0))

    def test_should_return_expected_data_all_anagrams_if_receive_a_list_of_anagrams(self):
        result = search_anagrams( input_data_all_anagrams )
        self.assertEqual(result, (expected_data_all_anagrams, 17))

    def test_should_return_empty_list_and_0_if_receive_list_without_anagrams(self):
        result = search_anagrams(["sort", "a"])
        self.assertEqual(result, ([], 0))

    def test_should_be_executed_in_less_than_1_8_seconds(self):
        start_time = time()
        search_anagrams( input_data )
        end_time = time()

        self.assertTrue( (end_time - start_time) < 1.8 )

    def test_should_return_type_exception_if_receive_None(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams(None)

    def test_should_return_type_exception_if_receive_string(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams("")

    def test_should_return_type_exception_if_receive_number(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams(0)

    def test_should_return_type_exception_if_receive_number_list(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams([0])
    
    def test_should_return_type_exception_if_receive_dict(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams({ "a": "b" })

class TestSearchAnagramsAdvanced(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_should_return_expected_data(self):
        result = search_anagrams_advanced( input_data )
        self.assertEqual(result, 
            (
                expected_data, 15, 
                "punctilio unpolitic", 
                "spate tapes tepas paste pates peats septa"
            )
        )
    
    def test_should_return_empty_values_if_receive_empty_list(self):
        result = search_anagrams_advanced([])
        self.assertEqual(result, ([], 0, "", ""))

    def test_should_return_empty_values_if_receive_list_without_anagrams(self):
        result = search_anagrams_advanced(["sort", "a"])
        self.assertEqual(result, ([], 0, "", ""))

    def test_should_return_empty_values_if_receive_list_with_a(self):
        result = search_anagrams_advanced(["a"])
        self.assertEqual(result, ([], 0, "", ""))

    def test_should_return_expected_data_all_anagrams_if_receive_a_list_of_anagrams(self):
        result = search_anagrams_advanced( input_data_all_anagrams )
        self.assertEqual(result,
            (
                expected_data_all_anagrams, 17,
                "kinship pinkish",
                "enlist inlets listen silent"
            )
        )

    def test_should_be_executed_in_less_than_1_8_seconds(self):
        start_time = time()
        search_anagrams_advanced( input_data )
        end_time = time()

        self.assertTrue( (end_time - start_time) < 1.8 )

    def test_should_return_type_exception_if_receive_None(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams_advanced(None)

    def test_should_return_type_exception_if_receive_string(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams_advanced("")
    
    def test_should_return_type_exception_if_receive_number(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams_advanced(0)

    def test_should_return_type_exception_if_receive_number_list(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams_advanced([0])

    def test_should_return_type_exception_if_receive_dict(self):
        with self.assertRaises(TypeError) as context:
            search_anagrams({ "a": "b" })

if __name__ == "__main__":
    main()