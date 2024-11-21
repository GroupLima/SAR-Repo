from rapidfuzz import process, fuzz
from basic_search import BasicSearch

class PhraseStartsWithSearch(BasicSearch):
    
    def __init__(self, **kwargs):
        self.query = kwargs.get('query'),
        self.qlen = kwargs.get('qlen')
        self.entries = kwargs.get('entries'),
        self.window_size = kwargs.get('window_size'),
        self.variance = kwargs.get('variance')
        
        super().__init__()

        self.populate_matches_dict()
        
        
    def find_matches_in(self, content):
        strings_to_compare = []
        #iterate through the whole content using self.window_size step
        #qlen is the length of the query
        # should be a match if query of specified variance is at the start of the substring

        #work in progress :')
        for i in range(0, len(content) - self.window_size + 1, self.window_size):
            string = content[i:i+self.window_size]
            strings_to_compare.append(string)
        matches = process.extract(self.query, strings_to_compare, scorer=fuzz.partial_ratio, score_cutoff=self.variance)
        for match, score, index in matches:
            string = strings_to_compare[index]
            if string.startswith(match):
                pass
        return matches