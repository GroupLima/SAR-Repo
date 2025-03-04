from rapidfuzz import process, fuzz
from basic_search_methods.Search_Method_Interface import Search_Method
import re

class Search_Word_Middle(Search_Method):
    
    def __init__(self, query, qlen, variance, json_entries, case_sensitive=False):
        self.query = query
        self.qlen = qlen
        self.variance = variance
        self.json_entries = json_entries
        self.case_sensitive = case_sensitive
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
            # query length is padded by 3 characters
            if (not word) or (len(word) < self.qlen-2):
                continue
    #crimgeou
            window_size = self.qlen
            word_size = len(word)

            best_score = 0
            # Check similarity score for words that may or may not match with the query
            # look through each word with steps and window size to find matching string
            for i in range(max(1, word_size-window_size+1)):
            
                if not self.case_sensitive:
                    score = get_fuzzy_score(word.lower(), i, min(word_size, i+window_size), self.query.lower())
                    #score = fuzz.ratio(self.query.lower(), word.lower()[i:i+window_size])
                else:
                    score = get_fuzzy_score(word, i, min(word_size, i+window_size), self.query)
                    #score = fuzz.ratio(self.query, word[i:i+window_size])

                if score > best_score:
                    best_score = score
            if best_score >= self.variance:
                results.append((word, best_score, index))
        return results

def get_words_to_compare(content):
    return [(word.group(), word.start()) for word in re.finditer(r'\S+', content)]

def word_too_short(word, qlen):
    # query length is padded by 3 characters
    return not word or len(word) < qlen - 2

def get_fuzzy_score(word, start_index, stop_index, query):
    return fuzz.ratio(query, word[start_index:stop_index])