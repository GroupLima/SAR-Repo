from rapidfuzz import process, fuzz
from basic_search_methods.Basic_Search_Interface import BasicSearch

class Search_Word_End(BasicSearch):
    
    def __init__(self, **kwargs):
        self.query = kwargs.get('query')
        self.qlen = kwargs.get('qlen')
        self.json_entries = kwargs.get('json_entries')
        self.window_size = kwargs.get('window_size')
        self.variance = kwargs.get('variance')
        
        super().__init__()


    def find_matches_in(self, content):
        """
        use rapid fuzz to extract all the matches in a single entry content
        specifically, use process.extract function and return the result
        """
        # write code here

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
            score = fuzz.ratio(self.query, word[len(word)-qlen:])

            if score >= self.variance:
                results.append((word, score, index))
        return results
        
        pass
