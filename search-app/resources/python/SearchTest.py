import unittest
from unittest.mock import patch
from resources.python.Search import Search
from resources.python.advanced_search import AdvancedSearch

# To run these tests, in ~/SAR-Repo/search-app, run the following command
# PYTHONPATH=./resources/python python3 -m unittest resources/python/SearchTest.py
class TestSearch(unittest.TestCase):

    def setUp(self):
        # basic search parameters for testing
        self.params_basic = {
            'qt': 'basic_search',  # query type
            'query': 'tribus',
            'rpp': 5,  # results per page
            'var': 100,  # variance
            'sm': 'phrase/keyword'  # search method
        }

    @patch('resources.python.Search.Search.load_json')
    def test_basic_search(self, mock_load_json):
        # load a mock json file instead of the actual file
        mock_load_json.return_value = {}

        search_instance = Search(self.params_basic)
        search_instance.init_basic_search_params()

        # tests if the search method is 'phrase/keyword'
        self.assertEqual(search_instance.search_method, 'phrase/keyword')

        # tests if the query is 'tribus'
        self.assertEqual(search_instance.query, 'tribus')

        # tests if the results per page is 5
        self.assertEqual(search_instance.results_per_page, 5)

if __name__ == '__main__':
    unittest.main()
