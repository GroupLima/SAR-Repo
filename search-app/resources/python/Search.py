import sys
from rapidfuzz import process, fuzz
"""
we using resources/json/entries.json to find matches

return example:
    {
    'ARO-1-0001-03' : {
        'accuracy score' : value,
        'match freq' : value
        'matches' : [
            (variance, start, end),
            (variance, start, end),
            (variance, start, end),
            (variance, start, end),
            (variance, start, end)
        ]
    }
    'ARO-1-0001-04' : [
        'accuracy score' : value,
        'match freq' : value
        'matches' : [
            (variance, start, end),
            (variance, start, end),
            (variance, start, end),
            (variance, start, end),
            (variance, start, end)
        ]
     'ARO-6-0001-01' : [
        'accuracy score' : value,
        'match freq' : value
        'matches' : [
            (variance, start, end),
            (variance, start, end),
            (variance, start, end),
            (variance, start, end),
            (variance, start, end)
        ]
    etc...
    }
"""

# Perform main search of compiled entry data
# Should consider splitting into 2 classes - one for file management to allow compounding of exact and match searches
class MatchData():
    
    search_methods = {
        0: 'regex',
        1: ''
    }
    
    def __init__(self, params, json_entries):
        #self.user_input = user_input # User string search
        
        self.json_entries = json_entries # returned data from search
        self.params = params
        
        #basic search params
        self.search_method = 0
        self.variance = 100 # default similarity of 100 (exact match) 
        self.transpositions = False # disable for more accurate results
        self.variance_limit = 50 # experiment with variance limit?
        self.results_per_page = 5 # default is 5 results per page
        
        self.matches = [] # return to search controller

        # initialize query and its length

        self.query = ''
        self.qlen = 0
        self.window_size = 5

        self.init_attributes()


    def init_attributes(self):
        try:
            self.query = self.params['q']
            self.qlen = len(self.qlen)
            if self.qlen <= 5:
                self.window_size = self.qlen
            else:
                self.window_size = self.qlen - (self.qlen / 2)
        except KeyError:
            raise KeyError()

    def convert_variance(self, perc_variance):
        """
        ranges from 0%-100% lower is closer to exact match; limit 100% has a low similarily of 50? experiment
        1. convert percentage to float value
        ex. 0% -> 100; 100% -> self.variance_limit
        2. assign result to self.variance
        """
        # write code here
        

        pass


    def order_by(self, match, sort_criteria):
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

    def calculate_accuracy_heuristic(self, match):
        """
        if exact match found, return 1

        """
        # write code here


        pass

    
    def find_matches(self, content):
        """
        use rapidfuzz for speed, scalability, and functionality

        """
        strings_to_compare = []
        #iterate through the whole content using self.window_size step
        for i in range(0, len(content), self.window_size):
            string = content[i:i + self.window_size]
            strings_to_compare.append(string)
        matches = process.extract(self.query, strings_to_compare, scorer=fuzz.ratio, score_cutoff=self.variance)
    
    # finds all matches
    def find_matches(self):
       
        
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