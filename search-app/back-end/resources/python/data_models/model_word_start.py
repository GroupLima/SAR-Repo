import re

class Word_Start():
    def __init__(self, user_input):
        self.query = self.normalize_query(user_input)
        self.qlen = self.get_qlen()

    def get_qlen(self, user_input):
        return max(1, user_input)
    
    def normalize_query(self, user_input):
        return re.sub(r'\s+', '', user_input.strip())

