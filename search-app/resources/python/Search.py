import sys
import json
from rapidfuzz import process, fuzz
from advanced_search import AdvancedSearch
from basic_search_methods.search_phrase_has_keywords import PhraseKeywordsSearch
from basic_search_methods.search_phrase_starts_with import PhraseStartsWithSearch
from basic_search_methods.search_phrase_contains import PhraseContainsSearch
from basic_search_methods.search_phrase_ends_with import PhraseEndsWithSearch
from basic_search_methods.search_regex import RegexSearch
import json_parser as jp

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

# for basic search and autocomplete
def basic_search(params):
    try:
        # write code here
        # find matches using search method chosen by user
        search = Search(params)
        search.init_basic_search_params()
        search.apply_basic_search()

        # sort entries by criteria param
        search.init_sort_params()
        search.order_by(search.sort_criteria)
        return search.get_matches()
    except Exception as e:
        print(
            f"Error initializing parameters or applying search. "
            f"Check parameter key names or search method. Details: {e}"
        )

    

def advanced_search(params):
    try:
        # write code here
        # filter which entries to find matches for
        search = Search(params)
        search.init_advanced_search_params()
        search.apply_advanced_search()

        # find matches using search method chosen by user
        search.init_basic_search_params()
        search.apply_basic_search()

        # sort entries by criteria param
        search.init_sort_params()
        search.order_by(search.sort_criteria)

        return search.get_matches()
    except Exception as e:
        print(
            f"Error initializing parameters or applying search. "
            f"Check parameter key names or search method. Details: {e}"
        )


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
    
    def __init__(self, params, json_entries, search_type):
        #self.user_input = user_input # User string search
        
        self.params = params
        # $param_keys = ['json', 'query', 'rpp', 'var', 'ob', 'sm', 'entry_id', 'date_from', 'date_to', 'vol', 'pg', 'pr', 'lang', 'page']

        # default advanced search params
        self.json_entries = None
        self.entry_id = ''
        self.date_from = None
        self.date_to = None
        self.vol = None
        self.pg = None
        self.lang = None
        
        # default basic search params
        self.search_method = 'exact match'
        self.search_class
        self.query = ''
        self.qlen = 0
        self.window_size = 5
        self.results_per_page = 5 # default is 5 results per page
        self.variance = 100 # default similarity of 100 (exact match)
        self.variance_limit = 50 # experiment with variance limit?

        # default sort params
        self.sort_criteria = ''
        
        self.matches = {} # return to search controller


    def init_advanced_search_params(self):
        """
        eg. self.entry_id = self.params['entry_id'] = 'ARO-6-'
        convert the values in the params to their types
        convert the values in each json entry to their types (could be done in json generator?)
        """
        # write code here
        raw_json_entries = self.params.get('json')
        if raw_json_entries:
            jp.parse_json(raw_json_entries)
            

        self.entry_id = self.params.get('entry_id')

        date_to_string = self.params.get('date_to')
        if date_to_string:
            self.date_to = jp.parse_date(date_to_string)

        date_to_string = self.params.get('date_to')

        vol_string = self.params.get('vol')
        if vol_string:
            jp.parse_num(vol_string)
            
        pg_string = self.params.get('pg')

        lang_string = self.params.get('lang')

        pass
  


    def apply_advanced_search(self, entry_id, date_from, date_to, language, volume, page, paragraph):
        """
        apply filters in order, return none if param is empty or nothing to filter
        only pass in params that are not None or ''
        use advanced_search.py
        """
        # write code here
        

        
        pass

    def get_args(self):
        args = {
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
            'sort_criteria': self.sort_criteria
        }
        return args


    def init_basic_search_params(self, params):
        """
        basic search params: query, var, sm, entry_id
        """
        # default number of results per page
        self.search_method = self.params['sm']

        # raise an error if the search method is not a key in search functions
        self.search_class = Search.search_classes.get(self.search_method)
        if not self.search_function:
            raise SearchMethodDoesNotExistError(self.search_method)
        
        self.query = self.params['query']

        if self.query != 'regex':
            self.qlen = len(self.query)
            self.set_window_size()
            
        self.result_per_page = self.params['rpp']
        self.convert_variance(params['var'])


    def set_window_size(self):
        """
        sets the value for what length the substring will cover over the text. It slides over the content
        
        eg. text = 'i like chocolate milk'
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
        """
        # write code here


        pass
        

    def convert_variance(self, perc_variance):
        """
        ranges from 0%-100% lower is closer to exact match; limit 100% has a low similarily of 50? experiment
        1. convert percentage to variance
        ex. 0% -> 100; 100% -> self.variance_limit
        2. assign result to self.variance
        """
        # write code here
        

        pass

    
    def apply_basic_search(self):
        """
        get the matches using search_classes
        """
        args = self.get_args()
        self.search_instance = globals()[self.search_class](**args)
        self.search_instance.get_matches()


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
    # cust_search = MatchData('holly')
    # cust_search.find_matches()
    if len(sys.argv > 1):
        params = sys.argv[1]
        obj = Search(params)
        matches = obj.get_matches()
        json.dumps(matches) # return the matches data in a JSON object
    pass