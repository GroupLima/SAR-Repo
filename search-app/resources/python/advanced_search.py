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

    # loop through all json entries
    # filter values of the json entries that match the param values
    def filter_entries(cls, json_objs, params=None):
        valid_entries = {}
        for entry_id, entry_data in json_objs.items():
            valid_entry = True
            for key, value in params.items():
                function_name = cls.function_names.get(key)

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
    parameters: date (tuple of ints: (year, month, date)), date_from (tuple of ints: (year, month, date))
    assume date_from is not None

    date value is in the form of a tuple of ints: (year, month, date)
    keep in mind some dates only have the year and month or even just the year
    """
    # write code here
    



    pass

def is_before_date(date, date_to) -> bool:
    """
    parameters: date (tuple of ints: (year, month, date)), date_to (tuple of ints: (year, month, date))
    assume date_to is not None

    date value is in the form of a tuple of ints: (year, month, date)
    keep in mind some dates only have the year and month or even just the year
    """
    # compares every entry to find if the user entered date is before 
    # return true if date is less than date_to
    match len(date_to):
        case 2:
            pass
        case 3 | 1:
            return date < date_to

def is_valid_language(language, language_param) -> bool:
    """
    parameters: language (string), language_param (string) 
    assume language and language_param are not None

    return true if the language_param is any
    otherwise return true if language matches the user param
    """
    # write code here
    if language == language_param:
        return True
    else:
        return False

def is_valid_volume(volume, volume_param) -> bool:
    """
    parameters: volume (int), volume_param (int)
    assume volume_param is not None

    return true if volume matches volume param
    """
    # write code here
    if volume == volume_param:
        return True
    else:
        return False

def is_valid_page(page, page_param) -> bool:
    """
    parameters: page (int), page_param (tuple of page ints: (1, 40, 28))
    assume page and page_param are not None
    
    if the page_param is invalid, handle appropriately
    check if page is in page_param
    """
    # write code here
    


    pass

# add more functions if required