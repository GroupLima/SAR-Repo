from abc import ABC, abstractmethod
from rapidfuzz import process, fuzz


"""
this is an abstract class (interface) where
any class that inherits this interface MUST 
implement its own version of the required 
functions aka anything that says @abstractmethod
"""
class BasicSearch(ABC):

    @abstractmethod
    def find_matches_in(self, content):
        """
        use rapid fuzz to extract all the matches in a single entry content
        specifically, use process.extract function and return the result
        dont implement anything here
        """
        pass