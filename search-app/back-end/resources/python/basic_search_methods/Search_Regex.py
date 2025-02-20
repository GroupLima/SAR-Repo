from rapidfuzz import process, fuzz
from basic_search_methods.Search_Method_Interface import Search_Method
import re

class Search_Regex(Search_Method):
    
    def __init__(self, query, qlen, json_entries):
        self.query = query
        self.qlen = qlen
        self.json_entries = json_entries
        
        super().__init__()


    def find_matches_in(self, content):
        """
        use rapid fuzz to extract all the matches in a single entry content
        specifically, use process.extract function and return the result
        """
        
        results = []
        matches = re.finditer(self.query, content)
        for match in  matches:
            results.append((match.group(), 100, match.span()[0]))
        return results
        
