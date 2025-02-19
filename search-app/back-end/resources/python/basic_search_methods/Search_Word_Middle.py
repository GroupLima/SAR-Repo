from rapidfuzz import process, fuzz
from basic_search_methods.Search_Method_Interface import Search_Method
import re

class Search_Word_Middle(Search_Method):
    
    def __init__(self, query, qlen, variance, json_entries):
        self.query = query
        self.qlen = qlen
        self.variance = variance
        self.json_entries = json_entries
        super().__init__()


    def find_matches_in(self, content):
        """
        use rapid fuzz to extract all the matches in a single entry content
        specifically, use process.extract function and return the result
        """
        # Extract words and their start indices
        words_to_compare = [(word.group(), word.start()) for word in re.finditer(r'\S+', content)]

        #work in progress :')
        results = []
        for word, index in words_to_compare:
            if not word or len(word) < self.qlen-2:
                continue

            window_size = self.qlen
            word_size = len(word)
            # Check similarity score for words that may or may not match with the query
            # look through each word with steps and window size to find matching string
            for i in range(word_size-window_size+1):
                score = fuzz.ratio(self.query, word[i:i+window_size])

                if score >= self.variance:
                    results.append((word, score, index))
                    break
        return results
