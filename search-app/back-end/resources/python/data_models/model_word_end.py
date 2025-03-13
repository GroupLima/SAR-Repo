import re

class Word_End():
    def __init__(self, user_input):
        self.query = self.normalize_query(user_input)
        self.qlen = self.get_qlen(self.query)

    def get_qlen(self, query):
        return max(1, len(query))
    
    def normalize_query(self, user_input):
        return re.sub(r'\s+', '', user_input.strip())

