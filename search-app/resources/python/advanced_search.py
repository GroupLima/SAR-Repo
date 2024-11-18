
# this file contains advanced search methods

class AdvancedSearch():
    function_names = {
        'entry_id' : 'is_valid_entry_id',
        'date_from' : 'is_after_date',
        'date_to' : 'is_before_date',
        'language' : 'is_valid_language',
        'volume' : 'is_valid_volume',
        'page' : 'is_valid_page',
        # add more functions names if required
    }

    # loop through all json entries
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

def is_valid_entry_id(value, id_pattern):
    return value in id_pattern

def is_after_date(value, date_from):
    pass

def is_before_date(value, date_to):
    pass

def is_valid_language(value, language):
    pass

def is_valid_volume(value, volume):
    pass

def is_valid_page(value, page):
    pass

# add more functions if required