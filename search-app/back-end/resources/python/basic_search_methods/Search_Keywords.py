from rapidfuzz import process, fuzz
from basic_search_methods.Search_Method_Interface import Search_Method

class Search_Keywords(Search_Method):
    def __init__(self, **kwargs):
        self.query = kwargs.get('query')
        self.json_entries = kwargs.get('json_entries')
        self.window_size = kwargs.get('window_size')
        self.variance = kwargs.get('variance')
        
        super().__init__()


    def find_matches_in(self, content):
        strings_to_compare = []
        #iterate through the whole content using self.window_size step
        for i in range(0, len(content), self.window_size):
            string = content[i:i + self.window_size]
            strings_to_compare.append(string)
        matches = process.extract(self.query, strings_to_compare, scorer=fuzz.ratio, score_cutoff=self.variance)

        return matches