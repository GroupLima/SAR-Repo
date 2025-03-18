import re

class Keywords():
    def __init__(self, user_input):
        self.query = self.normalize_query(user_input)
    
    def normalize_query(self, user_input):
        return re.sub(r'\s+', '', user_input.strip())