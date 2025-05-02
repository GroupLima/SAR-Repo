import sys
import json
from rapidfuzz import process, fuzz
from advanced_search import Advanced_Search
from basic_search import Basic_Search
import json_parser as Json_Parser
import sort_methods

from pathlib import Path



"""
we using resources/json/entries.json to find matches


params: user query, results per page, variance, order by asce/desc, search method, entry id, date from, date to, volume, page, paragraph, language, page number

search query steps:
    1. get search tools params
    2. page: get page, display results per page (params: results per page)
    3. where: filter advanced search (params: entry, date from, date to, volume, page, paragraph)
        order in which to filter the entries
        1. date
        2. language
        3. volume
        4. page
        6. paragraph
    4. match: find matches of similarity using simple search params (params: user query, search method, variance)
        search methods
        1. regex
        2. keyword
        3. starts with
        4. part of
        5. ends with
    5. order: order matches by params
        sort types:
            1. volume
            2. page
            3. date
        sort methods using sort types:
            0. most relevant first
            1. asc volume, page (first to last)
            2. desc volume, page (last to first)
            3. asc date (chronological order)
            4. desc date (most recent)
    6. highlight: set highlight tags around content matches
    7. suggest: enable suggestions


return example:
    {
    'ARO-1-0001-03' : {
        'accuracy_score' : value,
        'match_frequency' : value
        'matches' : [
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            ]
        }
    'ARO-1-0001-04' : {
        'accuracy_score' : value,
        'match_freq' : value
        'matches' : [
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            ]
        }
     'ARO-6-0001-01' : {
        'accuracy_score' : value,
        'match_freq' : value
        'matches' : [
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            ]
        }
    etc...
    }
"""

"""
def search(params):
    query_type = params['qt']
    match query_type:
        case 'basic_search':
            return basic_search(params)
        case 'advanced_search':
            return advanced_search(params)
        case _:
            print('search not found')
            return None
"""

            

"""
# for basic search and autocomplete
def basic_search(params):
    try:
        # write code here
        # find matches using search method chosen by user
        search = Search(params)
        search.init_basic_search_params()
        search.matches = search.apply_basic_search()
        #print(search.matches)
        # sort entries by criteria param
        search.init_sort_params()
        search.order_by(search.sort_criteria)
        return search
    except Exception as e:
        print(
            f"Error initializing parameters or applying search. "
            f"Check parameter key names or search method. Details: {e}"
        )

    
"""

"""
def advanced_search(params):
    try:
        # write code here
        # filter which entries to find matches for
        search = Search(params)
        search.init_advanced_search_params()
        search.apply_advanced_search()

        # find matches using search method chosen by user
        search.init_basic_search_params()
        search.matches = search.apply_basic_search()

        # sort entries by criteria param
        search.init_sort_params()
        search.order_by(search.sort_criteria)
        return search.get_matches()
    except Exception as e:
        print(
            f"Error initializing parameters or applying search. "
            f"Check parameter key names or search method. Details: {e}"
        )

"""


# Perform main search of compiled entry data
# Should consider splitting into 2 classes - one for file management to allow compounding of exact and match searches
class Search():
    

    search_classes = {
        # key = search method : value = tuple(class name, init variables)
        'phrase/keyword' : 'PhraseKeywordSearch',
        'starts with' : 'PhraseStartsWithSearch',
        'contains' : 'PhraseContainsSearch',
        'ends with' : 'PhraseEndsWithSearch',
        'regex' : 'RegexSearch',
    }
    
    def __init__(self, params, json_entries=None):
        #self.user_input = user_input # User string search
        
        self.params = params
        # $param_keys = ['json', 'query', 'rpp', 'var', 'ob', 'sm', 'entry_id', 'date_from', 'date_to', 'vol', 'page', 'pr', 'lang', 'page', 'sort']

        # default advanced search params
        self.json_entries = json_entries or self.load_json()
        self.entry_id = ''
        self.date_from = None
        self.date_to = None
        self.vol = None
        self.page = None
        self.lang = None
        
        # default basic search params
        self.search_method = 'word_start'
        self.search_class = ''
        self.query = ''
        self.case_sensitive = False
        self.qlen = 0
        self.window_size = 5
        self.min_step_size = 1 # non inclusive
        self.max_step_size = 6 # non inclusive
        self.step_size = 5 # always ranges between 2 and 5 inclusive
        self.results_per_page = 5 # default is 5 results per page
        self.variance = 100 # default similarity of 100 (exact match)
        self.variance_limit = 50 # experiment with variance limit?


        # default sort params
        self.sort_criteria = ()
        self.sort = 'Frequency within result'
        
        self.matches = {} # return to search controller

        #fix all of this later
        self.init_basic_search_params()
        self.init_advanced_search_params()
        #self.init_sort_params()
        #self.order_by(self.sort_criteria)

    def start(self):
        qt = self.params['qt'] # query type: basic or advanced

        if self.query != "*": # search term not empty, perform search
            search_obj = Basic_Search(self.search_method, self.query, self.variance, self.json_entries, self.case_sensitive) # pass in parameters for basic search
            self.matches = search_obj.find_matches()
        else: # matches is all entries
            for entry_id in self.json_entries.keys():
                    self.matches[entry_id] = {
                        'accuracy_score' : 100,
                        'match_frequency' : 0,
                        'matches' : []}
        # apply advance search filters:
        if qt == 'advanced_search':
            advs_entries = {}
            for entry_id in self.matches.keys(): # get json entries of the matches
                advs_entries[entry_id] = self.json_entries[entry_id]
            search_obj = Advanced_Search(self.lang, self.page, self.vol, self.entry_id, self.date_from, self.date_to)
            adv_matches = search_obj.filter_entries(advs_entries)
            for id in list(self.matches):
                if id not in adv_matches:
                    del self.matches[id] # remove entires that didnt pass the advv filters

        self.matches = self.sort_matches(self.matches)

        
        # self.matches = {'ARO-1-0001-03' : {
        #     'accuracy_score' : 20,
        #     'match_frequency' : 40,
        #     'matches' : []
        #     }
        # }
        

    def load_json(self):
        json_filepath = Path(__file__).resolve().parent.parent / 'json' / 'entries.json'
        with open(json_filepath, 'r') as json_file:
            json_entries = json.load(json_file)
        return json_entries

    def init_advanced_search_params(self):
        """
        eg. self.entry_id = self.params['entry_id'] = 'ARO-6-'
        convert the values in the params to their types
        convert the values in each json entry to their types (could be done in json generator?)
        """
        # write code here
        self.entry_id = self.params.get('entry_id')
        self.date_to = self.params.get('date_to')
        self.date_from = self.params.get('date_from')
        self.vol = self.params.get('vol')
        self.page = self.params.get('page')
        self.lang = self.params.get('lang')


    def init_basic_search_params(self):
        """
        basic search params: query, var, sm, entry_id
        """
        # set case sensitivity
        if self.params.get('case_sensitive') and self.params['case_sensitive'].lower() == 'true': self.case_sensitive = True
        # default number of results per page
        self.search_method = self.params['sm']
        # raise an error if the search method is not a key in search functions
        self.search_class = Search.search_classes.get(self.search_method)
        if not self.search_method:
            raise SearchMethodDoesNotExistError(self.search_method)
        
        self.query = self.params['query']
        # if self.query != 'regex':
        #     self.set_window_and_step()
            
        self.result_per_page = self.params['rpp']
        self.sort = self.params.get('sort') or self.sort
        self.convert_variance(self.params['var'])


    def convert_variance(self, variance):
        """
        ranges from 0%-100% lower is closer to exact match; limit 100% has a low similarily of 50? experiment
        1. convert percentage to variance
        ex. 0% -> 100; 100% -> self.variance_limit
        2. assign result to self.variance
        """
        # write code here
        variance = int(variance)
        #print(abs(variance*10 - 100))
        self.variance = abs(variance*10 - 100)

    def sort_matches(self, matches):
        # frequency, best, volumeasc, volumedsc, chronological
        match self.sort:
            case 'frequency':
                return sort_methods.sort_frequency(matches)
            case 'best':
                return sort_methods.sort_best_matches(matches)
            case _:
                return sort_methods.sort_best_matches(matches)

    def get_matches(self):
        return self.matches


class VarianceError(Exception): 
    def __init__(self, variance_limit):
        self.message = variance_limit + ' variance is too low'
        super().__init__(self.message)

class SearchTypeNotFoundError(Exception):
    def __init__(self, search_type):
        self.message = '\'' + search_type + '\'' + ' search type not found'
        super().__init__(self.message) 

class SearchMethodDoesNotExistError(Exception):    
    def __init__(self, search_method):
        self.message = '\'' + search_method + '\'' + ' search method does not exist'
        super().__init__(self.message) 

if __name__ == '__main__':
    if len(sys.argv) > 1:
        permitted = json.loads(sys.argv[1])
        #obj = search(permitted)
        search = Search(permitted)
        search.start()
        matches = search.get_matches()
        if matches:
            results = {"message": "matches found", "results": matches}
        else:
            results = {"message": "no matches found", "results": None}
        print(json.dumps(results)) # return the matches data in a JSON object
    else:
        arglen = len(sys.argv)
        results = {"message":  "Not enough arguments. Need parameters.", "results": arglen}
        print(json.dumps(results))
        #print(json.dumps({"error": "Not enough arguments. Need parameters."}))
    