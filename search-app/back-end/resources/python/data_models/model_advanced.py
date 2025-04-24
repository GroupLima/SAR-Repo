import re
from errors.custom_errors import InvalidAROFormatError
from errors.custom_errors import InvalidPageInputError
from errors.custom_errors import InvalidVolumeInputError
from errors.custom_errors import InvalidDateInputError
"""
A model that contains only the arguments required for Advanced Search. This will be used to determine
which search functions need to be executed.
"""

class AdvancedSearchModel():
    def __init__(self, language, pages, volumes, entry_id, date_from, date_to):
        #self.user_input = user_input # String
        #self.variants = variants # Integer
        #self.number_results = number_results # Integer
        #self.order_by = order_by # String

        #self.paragraph = paragraph # String or Null

        self.language = self.get_language(language) # String or Null
        self.pages = self.get_pages(pages) # Integer or Null
        self.volumes = self.get_volume(volumes) # Integer or Null
        self.entry_id = self.get_entry_id(entry_id) # String or Null
        self.date_from = self.get_date(date_from) # String or Null
        self.date_to = self.get_date(date_to) # String or Null
        

    def get_language(self, language):
        """
        parameters: language (string)
        assume language and is not None

        return the language if it is in list of valid languages
        otherwise return 'any' where no language filtering is required
        """
        valid_languages = {'latin':'la', 'scots':'sc', 'dutch':'nl', 'multiple':'mul'}
        return valid_languages[language] if language and language.lower() in valid_languages else 'any' # case insensitive
    
    def get_pages(self, pages):
        """
        parameters: pages (string of page ints: "1, 40, 28")
        assume page is not None
        
        convert into list of integer pages, removing spaces and commas
        """
        try:
            return set([page.strip() for page in pages.split(",")]) if pages else None
        except:
            raise InvalidPageInputError(pages)

    def get_volume(self, volumes):
        """
        parameters: volumes (list)
        assume volumes is not None

        set all volumes to int type and return if in valid volumes
        """
        # write code here

        valid_volumes = {1, 2, 4, 5, 6, 7, 8} # volume 3 does not exist
        if volumes is None: volumes = [1, 2, 4, 5, 6, 7, 8]
        try:
            volume_list = [int(volume) for volume in volumes]
            return set(volume for volume in volume_list if volume in valid_volumes) if volume_list else None
        except:
            raise InvalidVolumeInputError(volumes)

    def get_entry_id(self, entry_id):
        """
        parameters: entry_id (string), id_pattern_param (string)
        assume entry_id and id_pattern_param are not None

        check if pattern is valid using regex
        eg. if id_pattern_pattern is 'ARO-8'
        then a valid entry_id would be 'ARO-8-0021-03'
        """
        
        #write code here
        id_pattern = '^ARO-\d-\d{1,4}-\d{2}$'
        if not entry_id: return None
        if re.match(id_pattern, entry_id):
            return entry_id
        raise InvalidAROFormatError(entry_id)
    

    def get_date(self, date):
        #splits into 3 numbers: year, month, day
        try:
            if not date: return None
            parts = [int(num) for num in date.split("-")]
            if len(parts) != 3:
                return parts 
        except:
            raise InvalidDateInputError(date)