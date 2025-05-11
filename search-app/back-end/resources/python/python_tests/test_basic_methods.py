"""
1. search word start: get_words_to_compare, word_too_short, get_fuzzy_score, find_matches_in
2. search word middle
3. search word end
4. search keywords
5. search phrase
6. search regex
"""

import unittest
from unittest.mock import patch
import resources.python.basic_search_methods.Search_Keywords as Search_Keywords
import resources.python.basic_search_methods.Search_Phrase as Search_Phrase
import resources.python.basic_search_methods.Search_Regex as Search_Regex
import resources.python.basic_search_methods.Search_Word_End as Search_Word_End
import resources.python.basic_search_methods.Search_Word_Middle as Search_Word_Middle
import resources.python.basic_search_methods.Search_Word_Start as Search_Word_Start
from math import ceil
# To run these tests, in ~/SAR-Repo/search-app/back-end, run the following command
# PYTHONPATH=./resources/python python3 -m unittest resources.python.python_tests.test_basic_methods
class TestWordTooShort(unittest.TestCase):

    def test_word_too_short_start(self):
        qlen = 10
        self.assertTrue(Search_Word_Start.word_too_short('', qlen))
        self.assertTrue(Search_Word_Start.word_too_short('h', qlen))
        self.assertTrue(Search_Word_Start.word_too_short('holly', qlen))
        self.assertFalse(Search_Word_Start.word_too_short('hollyhollyholly', qlen))
        self.assertFalse(Search_Word_Start.word_too_short('hollyholly', qlen))

    def test_word_too_short_middle(self):
        qlen = 10
        self.assertTrue(Search_Word_Middle.word_too_short('', qlen))
        self.assertTrue(Search_Word_Middle.word_too_short('h', qlen))
        self.assertTrue(Search_Word_Middle.word_too_short('holly', qlen))
        self.assertTrue(Search_Word_Middle.word_too_short('hollyho', qlen))
        self.assertFalse(Search_Word_Middle.word_too_short('hollyhol', qlen))
        self.assertFalse(Search_Word_Middle.word_too_short('hollyholl', qlen))
        self.assertFalse(Search_Word_Middle.word_too_short('hollyholly', qlen))
        self.assertFalse(Search_Word_Middle.word_too_short('hollyhollyholly', qlen))

    def test_word_too_short_end(self):
        qlen = 10
        self.assertTrue(Search_Word_End.word_too_short('', qlen))
        self.assertTrue(Search_Word_End.word_too_short('h', qlen))
        self.assertTrue(Search_Word_End.word_too_short('holly', qlen))
        self.assertFalse(Search_Word_End.word_too_short('hollyhollyholly', qlen))
        self.assertFalse(Search_Word_End.word_too_short('hollyholly', qlen))

    def test_word_too_short_keywords(self):
        self.assertTrue(Search_Keywords.word_too_short(''))
        self.assertFalse(Search_Keywords.word_too_short('h'))
        self.assertFalse(Search_Keywords.word_too_short('hollyhollyholly'))

class TestFuzzyScore(unittest.TestCase):
    def setUp(self):
        self.query = "holly"
        self.qlen = len(self.query)

    # --- Search_Word_Start ---
    def test_start_exact_match(self):
        self.assertEqual(Search_Word_Start.get_fuzzy_score(self.query, self.qlen, "holly"), 100)

    def test_start_partial_match(self):
        self.assertGreater(Search_Word_Start.get_fuzzy_score(self.query, self.qlen, "hollywood"), 80)

    def test_start_mismatch(self):
        self.assertLess(Search_Word_Start.get_fuzzy_score(self.query, self.qlen, "zebra"), 10)

    # --- Search_Word_Middle ---
    def test_middle_exact_match(self):
        self.assertEqual(Search_Word_Middle.get_fuzzy_score("holly", 0, 5, self.query), 100)

    def test_middle_partial(self):
        self.assertGreater(Search_Word_Middle.get_fuzzy_score("ahollyb", 1, 6, self.query), 90)

    def test_middle_mismatch(self):
        self.assertLess(Search_Word_Middle.get_fuzzy_score("zebrah", 1, 5, self.query), 30)

    # --- Search_Word_End ---
    def test_end_exact_match(self):
        self.assertEqual(Search_Word_End.get_fuzzy_score(self.query, self.qlen, "oholly"), 100)

    def test_end_partial(self):
        self.assertGreater(Search_Word_End.get_fuzzy_score(self.query, self.qlen, "blahholly"), 90)

    def test_end_mismatch(self):
        self.assertLess(Search_Word_End.get_fuzzy_score(self.query, self.qlen, "carrot"), 20)

    # --- Search_Phrase ---
    def test_phrase_exact(self):
        self.assertEqual(Search_Phrase.get_fuzzy_score("hello world", "hello world"), 100)

    def test_phrase_partial(self):
        self.assertGreater(Search_Phrase.get_fuzzy_score("hello world", "hello brave new world"), 60)

    def test_phrase_mismatch(self):
        self.assertLess(Search_Phrase.get_fuzzy_score("hello world", "goodbye moon"), 30)

    # --- Search_Keywords ---
    def test_keywords_exact(self):
        self.assertEqual(Search_Keywords.get_fuzzy_score("python", "python"), 100)

    def test_keywords_close(self):
        self.assertGreater(Search_Keywords.get_fuzzy_score("python", "pythons"), 80)

    def test_keywords_wrong(self):
        self.assertLess(Search_Keywords.get_fuzzy_score("python", "zebra"), 20)


class TestGetWordsToCompare(unittest.TestCase):

    def test_simple_sentence_end(self):
        content = "hello world"
        expected = [("hello", 0), ("world", 6)]
        self.assertEqual(Search_Word_End.get_words_to_compare(content), expected)

    def test_simple_sentence_phrase(self):
        content = "hello world"
        expected = [("hello", 0, 5), ("world", 6, 11)]
        self.assertEqual(Search_Phrase.get_words_to_compare(content), expected)

    def test_multiple_spaces_end(self):
        content = "  this   has  multiple  spaces "
        expected = [("this", 2), ("has", 9), ("multiple", 14), ("spaces", 24)]
        self.assertEqual(Search_Word_End.get_words_to_compare(content), expected)

    def test_multiple_spaces_phrase(self):
        content = "  this   has  multiple  spaces "
        expected = [
            ("this", 2, 6),
            ("has", 9, 12),
            ("multiple", 14, 22),
            ("spaces", 24, 30)
        ]
        self.assertEqual(Search_Phrase.get_words_to_compare(content), expected)

    def test_tabs_and_newlines(self):
        content = "\tword1\nword2  \n\tword3"
        expected_end = [("word1", 1), ("word2", 7), ("word3", 16)]
        expected_phrase = [("word1", 1, 6), ("word2", 7, 12), ("word3", 16, 21)]
        self.assertEqual(Search_Word_End.get_words_to_compare(content), expected_end)
        self.assertEqual(Search_Phrase.get_words_to_compare(content), expected_phrase)

    def test_punctuation(self):
        content = "hello, world! how's everything?"
        expected_end = [
            ("hello,", 0),
            ("world!", 7),
            ("how's", 14),
            ("everything?", 20)
        ]
        expected_phrase = [
            ("hello,", 0, 6),
            ("world!", 7, 13),
            ("how's", 14, 19),
            ("everything?", 20, 31)
        ]
        self.assertEqual(Search_Word_End.get_words_to_compare(content), expected_end)
        self.assertEqual(Search_Phrase.get_words_to_compare(content), expected_phrase)

    def test_non_ascii(self):
        content = "café naïve résumé"
        expected_end = [("café", 0), ("naïve", 5), ("résumé", 11)]
        expected_phrase = [("café", 0, 4), ("naïve", 5, 10), ("résumé", 11, 17)]
        self.assertEqual(Search_Word_End.get_words_to_compare(content), expected_end)
        self.assertEqual(Search_Phrase.get_words_to_compare(content), expected_phrase)

    def test_emoji_and_symbols(self):
        content = "hello 👋 world 🌍👍"
        expected_end = [("hello", 0), ("👋", 6), ("world", 8), ("🌍👍", 14)]
        expected_phrase = [("hello", 0, 5), ("👋", 6, 7), ("world", 8, 13), ("🌍👍", 14, 16)]
        self.assertEqual(Search_Word_End.get_words_to_compare(content), expected_end)
        self.assertEqual(Search_Phrase.get_words_to_compare(content), expected_phrase)

    def test_empty_string(self):
        self.assertEqual(Search_Word_End.get_words_to_compare(""), [])
        self.assertEqual(Search_Phrase.get_words_to_compare(""), [])

    def test_only_spaces(self):
        self.assertEqual(Search_Word_End.get_words_to_compare("     "), [])
        self.assertEqual(Search_Phrase.get_words_to_compare("     "), [])

class TestSearchPhrase(unittest.TestCase):

    def test_get_word_count_margin(self):
        # Below all thresholds
        self.assertEqual(Search_Phrase.get_word_count_margin(1), 0)
        self.assertEqual(Search_Phrase.get_word_count_margin(2), ceil(2 * 0.1))
        self.assertEqual(Search_Phrase.get_word_count_margin(5), ceil(5 * 0.1))

        # Above 5
        self.assertEqual(Search_Phrase.get_word_count_margin(6), ceil(6 * 0.2))
        self.assertEqual(Search_Phrase.get_word_count_margin(10), ceil(10 * 0.2))

        # Above 10
        self.assertEqual(Search_Phrase.get_word_count_margin(11), ceil(11 * 0.3))
        self.assertEqual(Search_Phrase.get_word_count_margin(15), ceil(15 * 0.3))

        # Above 15
        self.assertEqual(Search_Phrase.get_word_count_margin(16), ceil(16 * 0.4))
        self.assertEqual(Search_Phrase.get_word_count_margin(20), ceil(20 * 0.4))

        # Above 20
        self.assertEqual(Search_Phrase.get_word_count_margin(21), ceil(21 * 0.6))
        self.assertEqual(Search_Phrase.get_word_count_margin(30), ceil(30 * 0.6))

    def test_is_overlapping(self):
        # Overlaps entirely
        self.assertTrue(Search_Phrase.is_overlapping(5, 10, 5, 10))
        # Partial overlaps
        self.assertTrue(Search_Phrase.is_overlapping(4, 8, 5, 10))  # Overlap at 5–8
        self.assertTrue(Search_Phrase.is_overlapping(8, 12, 5, 10))  # Overlap at 8–10
        self.assertTrue(Search_Phrase.is_overlapping(5, 12, 5, 10))  # Overlap at 5–10
        self.assertTrue(Search_Phrase.is_overlapping(2, 15, 5, 10))  # Overlap spans all
        # No overlap
        self.assertFalse(Search_Phrase.is_overlapping(0, 4, 5, 10))
        self.assertFalse(Search_Phrase.is_overlapping(11, 15, 5, 10))
        # Touching boundary (still not overlapping if exclusive)
        self.assertFalse(Search_Phrase.is_overlapping(10, 10, 11, 15))
        self.assertFalse(Search_Phrase.is_overlapping(0, 4, 4, 5))

class TestSearchMethods(unittest.TestCase):
    
    def setUp(self):
        # Mock data setup
        self.json_entries = [
            {"id": 1, "content": "This is a test sentence."},
            {"id": 2, "content": "Testing the search algorithm."},
            {"id": 3, "content": "A completely different string."}
        ]
        self.query = "test"
        self.variance = 80
        self.case_sensitive = False
        self.qlen = 4

    def test_search_keywords(self):
        search = Search_Keywords.Search_Keywords(self.query, self.variance, self.json_entries, self.case_sensitive)
        # Mocking the find_matches_in method's behavior
        result = search.find_matches_in(self.json_entries[0]["content"])
        
        # Check if results contain expected match
        self.assertGreater(len(result), 0, "No matches found!")
        self.assertTrue(all([score >= self.variance for _, score, _ in result]), "Some scores are below variance threshold.")
    
    def test_search_phrase(self):
        search = Search_Phrase.Search_Phrase(self.query, self.qlen, self.variance, self.json_entries, self.case_sensitive)
        result = search.find_matches_in(self.json_entries[0]["content"])

        self.assertGreater(len(result), 0, "No matches found!")
        self.assertTrue(all([score >= self.variance for _, score, _ in result]), "Some scores are below variance threshold.")
    
    def test_search_regex(self):
        regex_query = r"test"
        search = Search_Regex.Search_Regex(regex_query, self.json_entries)
        result = search.find_matches_in(self.json_entries[0]["content"])

        self.assertGreater(len(result), 0, "No regex matches found!")
        self.assertTrue(all([score == 100 for _, score, _ in result]), "Not all regex matches have score 100.")
    
    def test_search_word_end(self):
        search = Search_Word_End.Search_Word_End(self.query, self.qlen, self.variance, self.json_entries, self.case_sensitive)
        result = search.find_matches_in(self.json_entries[0]["content"])

        self.assertGreater(len(result), 0, "No matches found!")
        self.assertTrue(all([score >= self.variance for _, score, _ in result]), "Some scores are below variance threshold.")
    
    def test_search_word_middle(self):
        search = Search_Word_Middle.Search_Word_Middle(self.query, self.qlen, self.variance, self.json_entries, self.case_sensitive)
        result = search.find_matches_in(self.json_entries[0]["content"])

        self.assertGreater(len(result), 0, "No matches found!")
        self.assertTrue(all([score >= self.variance for _, score, _ in result]), "Some scores are below variance threshold.")
    
    def test_search_word_start(self):
        search = Search_Word_Start.Search_Word_Start(self.query, self.qlen, self.variance, self.json_entries, self.case_sensitive)
        result = search.find_matches_in(self.json_entries[1]["content"])

        self.assertGreater(len(result), 0, "No matches found!")
        self.assertTrue(all([score >= self.variance for _, score, _ in result]), "Some scores are below variance threshold.")

if __name__ == '__main__':
    unittest.main()
