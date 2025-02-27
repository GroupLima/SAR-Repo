from rapidfuzz import process, fuzz
from basic_search_methods.Search_Method_Interface import Search_Method
import re

class Search_Word_End(Search_Method):
    
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
        _content = content.lower() if self.case_sensitive else content
        # Extract words and their start indices
        words_to_compare = [(word.group(), word.start()) for word in re.finditer(r'\S+', content)]

        #work in progress :')
        results = []
        for word, index in words_to_compare:
            if word_too_short(word, self.qlen):
                continue
            # Check similarity score for words that may or may not match with the query
            # gets the first x number of characters of the word
            if not self.case_sensitive:
                score = get_fuzzy_score(self.query.lower(), self.qlen, word.lower())
                #score = fuzz.ratio(self.query.lower(), word.lower()[:min(len(self.query), len(word))])
            else:
                score = get_fuzzy_score(self.query, self.qlen, word)
                #score = fuzz.ratio(self.query, word[:min(len(self.query), len(word))])

            if score >= self.variance:
                results.append((word, score, index))
        return results

def get_words_to_compare(content):
    return [(word.group(), word.start()) for word in re.finditer(r'\S+', content)]

def word_too_short(word, qlen):
    return not word or len(word) < qlen

def get_fuzzy_score(query, qlen, word):
    return fuzz.ratio(query, word[len(word)-qlen:])
        
