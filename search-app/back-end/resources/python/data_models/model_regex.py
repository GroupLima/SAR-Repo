import re

class Regex():
    def __init__(self, user_input):
        self.query = self.normalize_query(user_input)
        self.qlen = self.get_qlen(user_input)

    def get_qlen(self, user_input):
        return max(1, len(user_input))
    
    def normalize_query(self, user_input):
        return re.sub(r'\s+', '', user_input.strip())

"""

"""

