from rapidfuzz import process, fuzz
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
            phrase_words = []
            start_pos = words_to_compare[i][1]
            for j in range(i, len(words_to_compare)):
                # different lengths of phrase
                phrase_words.append(words_to_compare[j][0])
                phrase = " ".join(phrase_words)

                if (len(phrase) > self.qlen*3) or ():
                    # skip phrases that are too long
                    break
                if len(phrase) < self.qlen/3:
                    # skip phrases that are too short
                    continue

                # Check similarity score for words that may or may not match with the query
                if not self.case_sensitive:
                    score = get_fuzzy_score(self.query.lower(), phrase.lower())
                else:
                    score = get_fuzzy_score(self.query, phrase)

                if score >= self.variance:
                    results.append((phrase, score, start_pos))
                    break # don't bother searching longer phrases

        return results

def get_words_to_compare(content):
    return [(word.group(), word.start()) for word in re.finditer(r'\S+', content)]

def get_fuzzy_score(query, phrase):
    return fuzz.ratio(query, phrase)