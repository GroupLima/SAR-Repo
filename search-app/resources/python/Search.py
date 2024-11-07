
import json
from pathlib import Path
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

# Perform main search of compiled entry data
class MatchData():
    
    entries_file = Path(__file__).resolve().parent.parent / 'json' / 'entries.json'
    
    def __init__(self, user_input):
        self.json_data = self.load_data(MatchData.entries_file)
        self.user_input = user_input # User string search
        self.entries = None # returned data from search
        #variance limit must be greater than 1
        self.variance_limit = 5
                
    def load_data(self, entries_file):
        try:
            with open(entries_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(entries_file + " not found")
            return None
            
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
    
    def get_matches(self):
        return self.entries

class VarianceError(Exception): 
    def __init__(self, variance_limit):
        self.message = variance_limit + ' variance is too low'
        super().__init__(self.message)      

if __name__ == '__main__':
    cust_search = MatchData('holly')
    cust_search.find_matches()