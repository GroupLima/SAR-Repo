from rapidfuzz import process, fuzz
from basic_search_methods.Search_Method_Interface import Search_Method
import re

class Search_Regex(Search_Method):
    
    def __init__(self, query, json_entries):
        self.query = query
        self.json_entries = json_entries
        
        super().__init__()


    def find_matches_in(self, content):
        """
        takes each entry and applys regex query
        """
        results = []
        matches = re.finditer(self.query, content)
        for match in  matches:
            results.append((match.group(), 100, match.span()[0]))
        return results
        
