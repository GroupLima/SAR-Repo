"""
A model that contains only the arguments required for Advanced Search. This will be used to determine
which search functions need to be executed.
"""

class AdvancedSearchModel():
    def __init__(self, user_input, variants, number_results, order_by, search_method, language, page, volume, paragraph, entry_id, from_date, to_date):
        self.user_input = user_input # String
        self.variants = variants # Integer
        self.number_results = number_results # Integer
        self.search_method = search_method # String
        self.order_by = order_by # String
        self.language = language # String or Null
        self.page = page # Integer or Null
        self.volume = volume # Integer or Null
        self.paragraph = paragraph # String or Null
        self.entry_id = entry_id # String or Null
        self.from_date = from_date # String or Null
        self.to_date = to_date # String or Null