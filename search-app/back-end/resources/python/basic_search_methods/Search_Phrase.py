from rapidfuzz import fuzz
from basic_search_methods.Search_Method_Interface import Search_Method
import re

class Search_Phrase(Search_Method):
    def __init__(self, query, qlen, variance, json_entries, case_sensitive=False):
        self.query = query
        self.qlen = qlen
        self.variance = variance
        self.json_entries = json_entries
        self.case_sensitive = case_sensitive
        super().__init__()

    def find_matches_in(self, content):
        """
        use rapid fuzz to extract all the phrase matches in a single entry content
        """
        results = []
        words_to_compare = get_words_to_compare(content)

        # basing the length of phrase on words rather than characters should save some
        # time, i think. There will be less iterations
        for i in range(len(words_to_compare)):
            start_pos = words_to_compare[i][1] # start from each word in entry
            best_score = 0 # the best scorring phrase from this starting point
            best_phrase = ""

            for j in range(i, len(words_to_compare)):
                # add a new word onto this phrase
                if j == 0:
                    phrase = words_to_compare[0][0]
                else:
                    phrase = phrase + " " + words_to_compare[j][0]

                # some phrases will never match so might as well skip what we can
                # otherwise, query will take ridiculous amount of time
                if (len(phrase) > self.qlen*2.5):
                    # phrase is too long, so stop checking from this start pos
                    break
                if len(phrase) < self.qlen/2.5:
                    # skip phrases that are too short
                    continue

                # Check similarity score for words that may or may not match with the query
                if not self.case_sensitive:
                    score = get_fuzzy_score(self.query.lower(), phrase.lower())
                else:
                    score = get_fuzzy_score(self.query, phrase)

                # check if this phrase matches better than previous ones:
                if score > best_score:
                    best_score = score
                    best_phrase = phrase

            if best_score >= self.variance: # add to list of matches
                results.append((best_phrase, best_score, start_pos))

        return results

def get_words_to_compare(content):
    return [(word.group(), word.start()) for word in re.finditer(r'\S+', content)]

def get_fuzzy_score(query, phrase):
    return fuzz.ratio(query, phrase)