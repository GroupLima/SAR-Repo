
import json
from pathlib import Path
import sys
"""
we using resources/json/entries.json to find matches

input: user input
return values: should return a dictionary of entry_ids 
where each entry has a dictionary of variances. each variance key 
has a list value containing the start and end indexes of each match

return example:
    {
    'ARO-1-0001-03' : [
        variance value 1: [
            (start index, end index),
            (start index, end index),
            (start index, end index),
            ],
        variance value 2: [
            (start index, end index),
            (start index, end index),
            (start index, end index),
            ],
        variance value 3: [
            (start index, end index),
            (start index, end index),
            (start index, end index),
            ],
        etc...
        ],
    'ARO-1-0001-04' : [
        variance value 1: [
            (start index, end index),
            (start index, end index),
            (start index, end index),
            ],
        variance value 2: [
            (start index, end index),
            (start index, end index),
            (start index, end index),
            ],
        variance value 3: [
            (start index, end index),
            (start index, end index),
            (start index, end index),
            ],
        ],
     'ARO-6-0001-01' : [
        variance value 1: [
            (start index, end index),
            (start index, end index),
            (start index, end index),
            ],
        variance value 2: [
            (start index, end index),
            (start index, end index),
            (start index, end index),
            ],
        variance value 3: [
            (start index, end index),
            (start index, end index),
            (start index, end index),
            ],
        etc...
        ],
    etc...
    }
"""

def load_data(self, entries_file):
    try:
        with open(entries_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(entries_file + " not found")
        return None

# Perform main search of compiled entry data
# Should consider splitting into 2 classes - one for file management to allow compounding of exact and match searches
class MatchData():
    
    entries_file = Path(__file__).resolve().parent.parent / 'json' / 'entries.json'

    search_methods = {
        0: 'sort_by_relevance',
        1: 'volume_[age]'
    }
    
    def __init__(self, params):
        self.json_data = self.load_data(MatchData.entries_file)
        #self.user_input = user_input # User string search
        self.entries = None # returned data from search
        self.params = params
        
        #basic search params
        #variance limit must be greater than 1
        self.search_method = 0
        self.variance = 0 # exact match
        self.results_per_page = 5 # default is 5 results per page
        self.order_by = 0 # most relevant first
            

    def dynamic_sort(self, entry, sort_criteria):
        # sort entries by sort criteria
        pass

    def find_variances(self):
        # Uses 
        pass

    def find_matches_by_variance(self, content, variance):
        # use regex
        pass
    
    # finds all matches
    def find_matches(self):
        #json_data = self.load_data(""ntries_file)
        try:
            # loops through the json
            for entry_id in self.json_data:
                # this is for an exact match
                # check from highest to lowest variance
                content = self.json_data[entry_id]['content']
                
                #initialize list of matches for an entry if one with highest variance found
                matches = self.find_matches_by_variance(content, self.variance_limit)
                if matches != []:
                    self.entries[entry_id] = [matches] # clear entry result of ba
                    
                    # check that the limit is more than 1
                    if self.variance_limit < 1:
                        raise VarianceError(self.variance_limit)
                    
                    # find more matches
                    for v in range(self.variance_limit-1, 0, -1):
                        matches.extend(self.find_matches_by_variance(content, v))
                
            print(self.entries)
        except:
            pass

    def apply_advanced_search(self, entry_id, date_from, date_to, language, volume, page, paragraph):
        # apply filters in order, return none if param is empty or nothing to filter
        json_data = load_data()
        # call advanced search from python file
        pass
    
    
    def get_matches(self, usery_query, search_method, variance):

        """
        #params: user query, results per page, variance, order by asce/desc, search method, entry id, date from, date to, volume, page, paragraph, language, page number
        
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
                2. exact matcg
                3. begins with
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
        """
        return self.entries
                           
    
    def get_basic_search_params(self, params):

        # default number of results per page
        result_per_page = params['r']

        params['r']
    
    # Search for exact matches of register - easy values such as ID, volume, page etc.
    def exact_search(self, entry_id=None, volume=None, page=None, chapter=None, lang=None, date=None):
        self.entry_id = entry_id # These are more for later use as a class, not needed in just a function
        self.volume = volume
        self.page = page
        self.chapter = chapter
        self.lang = lang
        self.date = date
                
        if entry_id != None and entry_id.isalnum(): # If they know exact entry ID just return the content for that, also small error checking
            return self.json_data[entry_id]['content']

        for entry_id, entry in self.json_data.items():
            # Need to check if the volume, page, chapter, lang, date are none. if not then go through every entry and add the json_data[entry_id] to a list. Need to ensure there is no repetition as if volume and page are specified then it should only return the entry once
            match_conditions = [
                (self.date is not None and str(self.date) == entry.get('date')),
                (self.volume is not None and str(self.volume) == entry.get('volume')),
                (self.page is not None and str(self.page) == entry.get('page')),
                (self.chapter is not None and str(self.chapter) == entry.get('chapter')),
                (self.lang is not None and str(self.lang) == entry.get('lang'))
            ]

            # If all conditions are true add the entry to the results
            if all(match_conditions):
                if entry_id not in self.entries:
                    self.entries[entry_id] = []
                self.entries[entry_id].append(entry)



class VarianceError(Exception): 
    def __init__(self, variance_limit):
        self.message = variance_limit + ' variance is too low'
        super().__init__(self.message)      

if __name__ == '__main__':
    # cust_search = MatchData('holly')
    # cust_search.find_matches()
    if len(sys.argv > 1):
        params = sys.argv[1]
        obj = MatchData(params)
        matches = obj.find_matches()
        json.dumps(matches) # return the matches data in a JSON object
    pass