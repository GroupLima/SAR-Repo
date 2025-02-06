"""
A model that contains only the arguments required for the search results. This will be used to determine
which search attributes of entries need to be displayed.
"""

class SearchResultsModel():
    def __init__(self, entry_id, date, language, content):
        self.entry_id = entry_id # String
        self.date = date # String or Null
        self.language = language # String or Null
        self.content = content # String or Null
            # content = {header, paragraph, annotations}