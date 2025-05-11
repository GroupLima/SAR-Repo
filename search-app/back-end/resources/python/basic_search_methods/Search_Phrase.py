from rapidfuzz import fuzz
from basic_search_methods.Search_Method_Interface import Search_Method
import re
from math import ceil

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
        word_count = len(self.query.split(" "))
        phrase_margin = get_word_count_margin(word_count)
        word_count_margin_max = word_count + phrase_margin if self.variance != 0 else word_count
        word_count_margin_min = word_count - phrase_margin if self.variance != 0 else word_count

        #index of a word in words to compare
        start_index = 0
        stop_index = 0
        phrase = ""
        
        best_score = 0
        best_phrase = ""

        #exact char in content
        phrase_start_index = 0
        phrase_stop_index = 0

        best_start_index = 0
        best_stop_index = 0

        word_counter = 0

        #keep track of best score until better score AND overlapping OR not overlapping anymore, if not overlapping, add phrase
        #while shorter than query, concatenate words
        while stop_index < len(words_to_compare):
            while word_counter < word_count_margin_max and stop_index < len(words_to_compare):
                #print("moving stop index: ", stop_index)
                phrase_stop_index = words_to_compare[stop_index][2]
                phrase = content[phrase_start_index:phrase_stop_index]
                
                # Check similarity score for words that may or may not match with the query
                if not self.case_sensitive:
                    score = get_fuzzy_score(self.query.lower(), phrase.lower())
                else:
                    score = get_fuzzy_score(self.query, phrase)

                
                # check if this phrase matches better than previous ones:
                overlapping = is_overlapping(start_index, stop_index, best_start_index, best_stop_index)
                #print("overlapping: ", overlapping)
                
                if (overlapping and score > best_score and score >= self.variance):
                    best_score = score
                    best_phrase = content[phrase_start_index:phrase_stop_index]
                    best_start_index = start_index
                    best_stop_index = stop_index

                elif not overlapping:
                    #add previous best score to results
                    if best_score != 0:
                        results.append((best_phrase, best_score, phrase_start_index))
                        best_score = 0
                        best_phrase = ""
                    #set new best score if matches variance
                    if score >= self.variance:
                        best_score = score
                        best_phrase = phrase
                        best_start_index = start_index
                        best_stop_index = stop_index
                stop_index += 1
                word_counter += 1
                #print("word_counter: ", word_counter)
            #while longer than query, remove words
            while word_counter >= word_count_margin_min:
                #print("moving start index: ", start_index)
                phrase_start_index = words_to_compare[start_index][1]
                #shift the start point to the start of the next word
                phrase = content[phrase_start_index:phrase_stop_index]
                
                # Check similarity score for words that may or may not match with the query
                if not self.case_sensitive:
                    score = get_fuzzy_score(self.query.lower(), phrase.lower())
                else:
                    score = get_fuzzy_score(self.query, phrase)

                
                # check if this phrase matches better than previous ones:
                overlapping = is_overlapping(start_index, stop_index, best_start_index, best_stop_index)

                if (overlapping and score > best_score and score >= self.variance):
                    best_score = score
                    best_phrase = phrase
                    best_start_index = start_index
                    best_stop_index = stop_index

                elif not overlapping:
                    #add previous best score to results
                    if best_score != 0:
                        results.append((best_phrase, best_score, phrase_start_index))
                        best_score = 0
                        best_phrase = ""
                    #update new best score if matches variance
                    if score >= self.variance:
                        best_score = score
                        best_phrase = content[phrase_start_index:phrase_stop_index]
                        best_start_index = start_index
                        best_stop_index = stop_index
                start_index += 1
                word_counter -= 1

        if best_score != 0:
            results.append((best_phrase, best_score, words_to_compare[best_start_index][1]))
        return results

def get_words_to_compare(content):
    return [(word.group(), word.start(), word.end()) for word in re.finditer(r'\S+', content)]

def get_fuzzy_score(query, phrase):
    return fuzz.ratio(query, phrase)

def get_word_count_margin(query_word_count):

    #increase margin for longer phrases
    word_margin = 0
    if query_word_count > 20:
        word_margin = ceil(query_word_count*0.6)
    elif query_word_count > 15:
        word_margin = ceil(query_word_count*0.4)
    elif query_word_count > 10:
        word_margin = ceil(query_word_count*0.3)
    elif query_word_count > 5:
        word_margin = ceil(query_word_count*0.2)
    elif query_word_count > 1:
        word_margin = ceil(query_word_count*0.1)
    return word_margin

def is_overlapping(start_index, stop_index, best_start_index, best_stop_index):
    # check if the start and stop indices of the current phrase overlap with the best phrase
    return (start_index < best_stop_index and stop_index > best_start_index)

