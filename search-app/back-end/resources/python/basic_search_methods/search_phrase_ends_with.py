from rapidfuzz import process, fuzz
from basic_search_methods.basic_search import BasicSearch

class PhraseEndsWithSearch(BasicSearch):
    
    def __init__(self, **kwargs):
        self.query = kwargs.get('query')
        self.qlen = kwargs.get('qlen')
        self.json_entries = kwargs.get('json_entries')
        self.window_size = kwargs.get('window_size')
        self.variance = kwargs.get('variance')
        
        super().__init__()

        self.populate_matches_dict()


    def find_matches_in(self, content):
        """
        use rapid fuzz to extract all the matches in a single entry content
        specifically, use process.extract function and return the result
        """
        # write code here


        
        pass
