import re
from errors.custom_errors import InvalidAROFormatError
from errors.custom_errors import InvalidPageInputError
from errors.custom_errors import InvalidVolumeInputError

"""
A model that contains only the arguments required for Advanced Search. This will be used to determine
which search functions need to be executed.
"""

class AdvancedSearchModel():
    def __init__(self, language, page, volume, entry_id, date_from, date_to):
        #self.user_input = user_input # String
        #self.variants = variants # Integer
        #self.number_results = number_results # Integer
        #self.order_by = order_by # String

        #self.paragraph = paragraph # String or Null

        self.language = self.get_language(language) # String or Null
        self.page = self.get_pages(page) # Integer or Null
        self.volume = self.get_volume(volume) # Integer or Null
        self.entry_id = self.get_entry_id(entry_id) # String or Null
        self.from_date = self.get_date_from(date_from) # String or Null
        self.to_date = self.get_date_to(date_to) # String or Null
        

    def get_language(self, language) -> str:
        """
        parameters: language (string)
        assume language and is not None

        return the language if it is in list of valid languages
        otherwise return 'any' where no language filtering is required
        """
        valid_languages = {'latin', 'middle scots', 'dutch'}
        return language if language.lower() in valid_languages else 'any' # case insensitive
    
    def get_pages(self, pages) -> set:
        """
        parameters: pages (string of page ints: "1, 40, 28")
        assume page is not None
        
        convert into list of integer pages, removing spaces and commas
        """
        try:
            return set([int(page.strip()) for page in pages.split(",")])
        except:
            raise InvalidPageInputError(pages)

    def get_volume(self, volumes) -> set:
        """
        parameters: volumes (tuple)
        assume volumes is not None

        set all volumes to int type and return if in valid volumes
        """
        # write code here
        valid_volumes = {1, 2, 4, 5, 6, 7, 8} # volume 3 does not exist

        try:
            return set([int(volume) for volume in volumes if int(volume) in valid_volumes])
        except:
            raise InvalidVolumeInputError(volumes)

    def get_entry_id(self, entry_id) -> str:
        """
        parameters: entry_id (string), id_pattern_param (string)
        assume entry_id and id_pattern_param are not None

        check if pattern is valid using regex
        eg. if id_pattern_pattern is 'ARO-8'
        then a valid entry_id would be 'ARO-8-0021-03'
        """
        
        #write code here
        id_pattern = '^ARO-\d-\d{1,4}-\d{2}$'
        
        if re.match(entry_id, id_pattern) or not entry_id:
            return entry_id
        raise InvalidAROFormatError(entry_id)
    

    def get_date(self, date):
        #already 3 tuple
        return date