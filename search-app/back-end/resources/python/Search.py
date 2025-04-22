import sys
import json
from rapidfuzz import process, fuzz
from advanced_search import Advanced_Search
from basic_search import Basic_Search
import json_parser as Json_Parser

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
        # $param_keys = ['json', 'query', 'rpp', 'var', 'ob', 'sm', 'entry_id', 'date_from', 'date_to', 'vol', 'pg', 'pr', 'lang', 'page']

        # default advanced search params
        self.json_entries = json_entries or self.load_json()
        self.entry_id = ''
        self.date_from = None
        self.date_to = None
        self.vol = None
        self.pg = None
        self.lang = None
        
        # default basic search params
        self.search_method = 'word_start'
        self.search_class = ''
        self.query = ''
        self.qlen = 0
        self.window_size = 5
        self.min_step_size = 1 # non inclusive
        self.max_step_size = 6 # non inclusive
        self.step_size = 5 # always ranges between 2 and 5 inclusive
        self.results_per_page = 5 # default is 5 results per page
        self.variance = 100 # default similarity of 100 (exact match)
        self.variance_limit = 50 # experiment with variance limit?


        # default sort params
        self.sort_criteria = ''
        
        self.matches = {} # return to search controller

        #fix all of this later
        self.init_basic_search_params()
        #self.init_advanced_search_params()
        #self.init_sort_params()
        #self.order_by(self.sort_criteria)

    def start(self):
        qt = self.params['qt'] # query type: basic or advanced
        
        search_obj = Basic_Search(self.search_method, self.query, self.variance, self.json_entries) # pass in parameters for basic search
        self.matches = search_obj.find_matches()
        
        if qt == 'advanced_search':
            advs_entries = {}
            for entry_id,  in self.matches:
                advs_entries[entry_id] = self.json_entries[entry_id]
            search_obj = Advanced_Search(self.params)
            self.matches = search_obj.filter_entries(advs_entries)
        
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
        self.date_to = Json_Parser.parse_date(self.params.get('date_to'))
        self.date_from = Json_Parser.parse_date(self.params.get('date_from'))
        self.vol = Json_Parser.parse_num(self.params.get('vol'))
        self.pg = Json_Parser.parse_num(self.params.get('pg'))
        self.lang = Json_Parser.parse_num(self.params.get('lang'))
  

    def apply_advanced_search(self, entry_id, date_from, date_to, language, volume, page, paragraph):
        """
        apply filters in order, return none if param is empty or nothing to filter
        only pass in params that are not None or ''
        use advanced_search.py
        """
        # write code here

        pass
    """
    def get_args(self):
        args = {
            'json_entries' : self.json_entries,
            'entry_id': self.entry_id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'vol': self.vol,
            'pg': self.pg,
            'lang': self.lang,
            'search_method': self.search_method,
            'query': self.query,
            'qlen': self.qlen,
            'window_size': self.window_size,
            'results_per_page': self.result_per_page,
            'variance': self.variance,
            'variance_limit': self.variance_limit,
            'ob': self.sort_criteria
        }
        return args
    """
    


    def init_basic_search_params(self):
        """
        basic search params: query, var, sm, entry_id
        """
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
        self.convert_variance(self.params['var'])

    """
    def set_window_and_step(self):
            """"""
            sets the value for what length the substring will cover over the text. It slides over the content
            
            eg. text = 'i like chocolate milk'
            use input = 'chalk'
            window size = 4
            step size = 3

            start
            iteration 0: windowed text = '[i li]ke chocolate milk', substring = 'i li'
            iteration 1: windowed text = 'i l[ike ]chocolate milk', substring = 'ike '
            iteration 2: windowed text = 'i like[ cho]colate milk', substring = ' cho'
            iteration 3: windowed text = 'i like ch[ocol]ate milk', substring = 'ocol'
            iteration 4: windowed text = 'i like choco[late] milk', substring = 'late'
            iteration 5: windowed text = 'i like chocolat[e mi]lk', substring = 'e mi'
            end

            then the query will be compared with each of the substrings and determine if its a match
            """"""
            # write code here
            self.qlen = len(self.query)
            self.window_size = max(len(self.query), 1)
            self.step_size = max(self.min_step_size, min(self.window_size, self.max_step_size))


            pass
        """
    
        

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

    """
     def apply_basic_search(self):
        
        #get the matches using search_classes
        
        args = self.get_args()
        self.search_instance = globals()[self.search_class](**args)
        return self.search_instance.get_matches()


    """
   
    def init_sort_params(self):
        """
        index params using 'ob' to get the string value of the sort type
        assign self.sort_criteria tuple values value of the values and whether its ascending or descending
        eg. self.sort_criteria = (  
                                    (date, ascending), 
                                    (best matches, descending), 
                                    (frequency in result, descending)
                                )
        """
        # write code here


        pass

    def order_by(self, sort_criteria):
        """
        sort entries by sort criteria (tuple)
        direction criteria: ascending, descending
        params criteria: volume, page, date
        date and volume are mutally exclusive
        possible combinations:  (volume, page, ascending),
                                (volume, page, descending),
                                (date, ascending), #oldest to most recent
                                (date, descending) #most recent to oldest
                                (frequency in result)
                                (best matches)
        if volume, page are the same or date is the same, then sort by best match
        if frequency in result is the same, then sort by best match
        if match accuracy is the same, then sort by frequency
        if sort_criteria not frequency_in_result: (criteria, matches accuracy descending, frequency descending)
        if sort_criteria is frequency_in_result: (frequency descending, accuracy)
        """
        # write code here
            

        pass


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
    