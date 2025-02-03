import re
# this file contains advanced search methods

class AdvancedSearch():
    function_names = {
        'entry_id' : 'is_valid_entry_id',
        'date_from' : 'is_after_date',
        'date_to' : 'is_before_date',
        'lang' : 'is_valid_language',
        'vol' : 'is_valid_volume',
        'pg' : 'is_valid_page',
        # add more functions names if required
    }

    def __init__(self, json_objs, params=None):
        self.filter_entries(json_objs, params)

    # loop through all json entries
    # filter values of the json entries that match the param values
    def filter_entries(self, json_objs, params=None):
        valid_entries = {}

        for entry_id, entry_data in json_objs.items():
            valid_entry = True
            for key, value in params.items():
                function_name = AdvancedSearch.function_names.get(key)

                # check if key exists in entry_data
                entry_value = entry_data.get(key)
                if entry_value is None:
                    valid_entry = False
                    break
                
                if function_name:
                    valid_entry = getattr(AdvancedSearch, function_name)(entry_data[key], value)
                else:
                    return {}
            # add valid entry to return item
            if valid_entry:
                valid_entries[entry_id] = entry_data
        
        return valid_entries

def is_valid_entry_id(entry_id, id_pattern_param) -> bool:
    """
    parameters: entry_id (string), id_pattern_param (string)
    assume entry_id and id_pattern_param are not None

    check if pattern is valid using regex
    eg. if id_pattern_pattern is 'ARO-8'
    then a valid entry_id would be 'ARO-8-0021-03'
    """
    #write code here
    if re.match(entry_id, id_pattern_param):
        return True
    else:
        return False
    

def is_after_date(date, date_from) -> bool:
    """
    parameters: date (tuple of ints: (year, month, day)), date_from (tuple of ints: (year, month, date))
    assume date_from is not None

    date value is in the form of a tuple of ints: (year, month, date)
    #date_from param always has all 3 ints
    keep in mind some dates in the json file only have the year and month or even just the year
    returns true for dates after and not including date_from
    """
    # write code here
    #year, month, day
    #0000 00 00
    #2^7, 2^3, 2^1
    date_int = 0
    date_int += date[0] << 7
    if len(date) > 1:
        date_int += date[1] << 3
        if len(date) > 2:
            date_int += date[2]
    date_from_int = (date_from[0] << 7) + (date_from[1] << 3) + (date_from[2])
    return date_int > date_from_int


def is_before_date(date, date_to) -> bool:
    """
    parameters: date (tuple of ints: (year, month, day)), date_to (tuple of ints: (year, month, day))
    assume date_to is not None

    date value is in the form of a tuple of ints: (year, month, day)
    keep in mind some dates only have the year and month or even just the year
    returns true for dates before and not including date_to
    """
    # compares every entry to find if the user entered date is before 
    # return true if date is less than date_to
    #year, month, day
    #0000 00 00
    #2^7, 2^3, 2^1
    date_int = 0
    date_int += date[0] << 7
    if len(date) > 1:
        date_int += date[1] << 3
        if len(date) > 2:
            date_int += date[2]
    date_to_int = (date_to[0] << 7) + (date_to[1] << 3) + (date_to[2])
    return date_int < date_to_int

def is_valid_language(language, language_param) -> bool:
    """
    parameters: language (string), language_param (string) 
    assume language and language_param are not None

    return true if the language_param is any
    otherwise return true if language matches the user param
    """
    return language == language_param


def is_valid_volume(volume, volume_param) -> bool:
    """
    parameters: volume (int), volume_param (int)
    assume volume_param is not None

    return true if volume matches volume param
    """
    # write code here
    return volume == volume_param


def is_valid_page(page, page_param) -> bool:
    """
    parameters: page (int), page_param (tuple of page ints: (1, 40, 28))
    assume page and page_param are not None
    
    check if page is in page_param
    """
    return page in page_param

def get_date_int(date):
    date_int = 0
    date_int += date[0] << 7
    if len(date) > 1:
        date_int += date[1] << 3
        if len(date) > 2:
            date_int += date[2]
    return date_int


# add more functions if required