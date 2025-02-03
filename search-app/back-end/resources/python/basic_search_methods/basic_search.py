from abc import ABC, abstractmethod
from rapidfuzz import process, fuzz

class BasicSearch(ABC):

    @abstractmethod
    def __init__(self):
        self.matches = {}
        

    @abstractmethod
    def find_matches_in(self, content):
        """
        use rapid fuzz to extract all the matches in a single entry content
        specifically, use process.extract function and return the result
        """
        pass


    def populate_matches_dict(self):
        """
        iterate through the key value pairs of entries dictionary and find the matches for each entry.
        if find_matches_in returns en empty list, don't add anything to the self.matches dictionary
        otherwise, create a new key value pair in self.matches with entry_id as the key and matches as the value
        """
        for entry_id, data in self.json_entries.items():
            
            content = data['content']
            matches = self.find_matches_in(content)
            if matches:
                accuracy_score = self.calculate_accuracy_heuristic(matches)
                match_frequency = len(matches)
                self.matches[entry_id] = {
                    'accuracy_score' : accuracy_score,
                    'match_frequency' : match_frequency,
                    'matches' : matches
                }
        pass


    def get_matches(self):
        """
        return self.matches dictionary
        """
        return self.matches


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
