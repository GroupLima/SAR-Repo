from rapidfuzz import process, fuzz
from basic_search_methods.Search_Method_Interface import Search_Method
import re

class Search_Keywords(Search_Method):
    def __init__(self, query, variance, json_entries, case_sensitive=False):
        self.query = query
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
        words_to_compare = get_words_to_compare(content)
    
        results = []
        # separate query into words
        query_words = self.query.split()
        for word, index in words_to_compare:
            for query_word in query_words:
                if word_too_short(word):
                    continue
                # Check similarity score for words that may or may not match with the query
                if not self.case_sensitive:
                    score = get_fuzzy_score(query_word.lower(), word.lower())
                else:
                    score = get_fuzzy_score(query_word, word)

                if score >= self.variance:
                    results.append((word, score, index))
        return results

def get_words_to_compare(content):
    return [(word.group(), word.start()) for word in re.finditer(r'\S+', content)]

def word_too_short(word):
    return not word

def get_fuzzy_score(query, word):
    return fuzz.ratio(query, word)