from rapidfuzz import process, fuzz
from basic_search_methods.Search_Method_Interface import Search_Method
import re

class Search_Word_Start(Search_Method):

    def __init__(self, query, qlen, variance, json_entries, case_sensitive=False):
        self.query = query
        self.qlen = qlen
        self.variance = variance # Integer
        self.json_entries = json_entries
        self.case_sensitive = case_sensitive
        super().__init__()
        
    def find_matches_in(self, content):
        # Extract words and their start indices
        words_to_compare = [(word.group(), word.start()) for word in re.finditer(r'\S+', content)]
        #work in progress :')
        results = []
        for word, index in words_to_compare:
            if not word or len(word) < self.qlen-2:
                continue
            # Check similarity score for words that may or may not match with the query
            # gets the first x number of characters of the word
            if not self.case_sensitive:
                score = fuzz.ratio(self.query.lower(), word.lower()[:min(len(self.query), len(word))])
            else:
                score = fuzz.ratio(self.query, word[:min(len(self.query), len(word))])

            if score >= self.variance:
                results.append((word, score, index))
        return results