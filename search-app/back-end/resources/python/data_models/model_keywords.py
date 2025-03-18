import re

class Keywords():
    def __init__(self, user_input):
        self.query = self.normalize_query(user_input)
    
    def normalize_query(self, user_input):
        return user_input.strip() # get rid of trailing and leading spaces