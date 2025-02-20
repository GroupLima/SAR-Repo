"""
A model that contains only the arguments required for Basic Search. This will be used to determine
which search functions need to be executed.
"""
from data_models.model_word_start import Word_Start
from data_models.model_word_middle import Word_Middle
from data_models.model_word_end import Word_End
# from model_phrase import Phrase
from data_models.model_keywords import Keywords
from basic_search_methods.Search_Word_Start import Search_Word_Start
from basic_search_methods.Search_Word_Middle import Search_Word_Middle
from basic_search_methods.Search_Word_End import Search_Word_End
from basic_search_methods.Search_Regex import Search_Regex
from basic_search_methods.Search_Keywords import Search_Keywords
# from basic_search_methods.Search_Phrase import Search_Phrase

class Basic_Search():
    def __init__(self, search_method, user_input, variance, json_entries):
        self.user_input = user_input # String
        self.variance = variance # Integer
        self.search_method = search_method # String
        self.json_entries = json_entries

    def find_matches(self):
        search = None
        results = None
        match(self.search_method):
            case 'word_start':
                #deserialize arguments for each search
                args = Word_Start(self.user_input)
                #pass deserialized arguments into corresponding function
                search = Search_Word_Start(args.query, args.qlen, self.variance, self.json_entries)
            case 'word_middle':
                args = Word_Middle(self.user_input)                  
                search = Search_Word_Middle(args.query, args.qlen, self.variance, self.json_entries)
            case 'word_end':
                args = Word_End(self.user_input)
                search = Search_Word_End(args.query, args.qlen, self.variance, self.json_entries)
            case 'regex':
                search = Search_Regex(self.user_input, self.json_entries)
            case 'keywords':
                args = Keywords(args.query)
                search = Search_Keywords() 
            case _:
                print('search method not specified')

        if search: results = self.get_formatted_matches(search) #return result (for example to advanced search so it can apply the rest of the filters)
        return results
            
    def get_formatted_matches(self, search):
        """
        iterate through the key value pairs of entries dictionary and find the matches for each entry.
        if find_matches_in returns an empty list, don't add anything to the self.matches dictionary
        otherwise, create a new key value pair in self.matches with entry_id as the key and matches as the value
        """
        results = {}
        for entry_id, data in self.json_entries.items():
            content = data['content']
            matches = search.find_matches_in(content)
            if matches:
                accuracy_score = self.calculate_accuracy_heuristic(matches)
                match_frequency = len(matches)
                results[entry_id] = {
                    'accuracy_score' : accuracy_score,
                    'match_frequency' : match_frequency,
                    'matches' : matches
                }
        
        return results

    def calculate_accuracy_heuristic(self, matches):
        """
        if exact match found, return 100

        """
        # write code here
        n = len(matches)
        total_score = 0
        for match in matches:
            similarity_score = match[1]
            if similarity_score == 100:
                return 100
            else:
                total_score += similarity_score
        return total_score / n




