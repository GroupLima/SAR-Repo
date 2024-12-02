from rapidfuzz import process, fuzz
from basic_search_methods.basic_search import BasicSearch
import re

class PhraseStartsWithSearch(BasicSearch):

    def __init__(self, **kwargs):
        self.query = kwargs.get('query')
        self.normalized_query = re.sub(r'\s+', '', self.query.strip())
        self.qlen = max(1, kwargs.get('qlen', 1))
        self.json_entries = kwargs.get('json_entries')
        self.window_size = kwargs.get('window_size')
        self.step_size = kwargs.get('step_size')
        self.variance = kwargs.get('variance')
        super().__init__()

        self.populate_matches_dict()
        
    def find_matches_in(self, content):
        # Extract words and their start indices
        strings_to_compare = [(match.group(), match.start()) for match in re.finditer(r'\b\w+\b', content)]

        #print(strings_to_compare)
        #print(strings_to_compare)
        #iterate through the whole content using self.window_size step
        #qlen is the length of the query
        # should be a match if query of specified variance is at the start of the substring

        #work in progress :')
        results = []
        for substring, index in strings_to_compare:
            if not substring or len(substring) < self.qlen-2:
                continue
            # Check similarity score for strings starting with the query
            score = fuzz.ratio(self.normalized_query, substring[:min(len(self.normalized_query), len(substring))])
            #score = self.calculate_combined_score(self.query.strip(), substring[:len(self.query.strip())])
            if score >= self.variance:
                results.append((substring, score, index))
        return results