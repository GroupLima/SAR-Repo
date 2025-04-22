import re
from data_models.model_advanced import AdvancedSearchModel
from advanced_search_methods import AdvancedSearchMethods

""" This class is executes the Advanced Search Filters for Entry ID, Language, Date, Volume and Page. """

class Advanced_Search():
    def __init__(self, params=None):
        self.params = params # input parameters from the user query

    # filter values of the json entries that match the param values
    def filter_entries(self, json_entries):
        args = AdvancedSearchModel( # format/parse and validate the input parameters
            language = self.params['lang'], 
            pages = self.params['pg'], 
            volumes = self.params['vol'], 
            entry_id = self.params['entry_id'],
            date_from = self.params['date_from'], 
            date_to = self.params['date_to']
        )

        # loop through all json entries
        valid_entries = {}
        for entry_id, entry_data in json_entries.items():
            if self.is_valid_entry(args, entry_data):
                valid_entries[entry_id] = entry_data
        
        return valid_entries
    
    def is_valid_entry(self, args, entry_data):
        # check whether the given input arguments match the entry attributes
        if not entry_data.get('lang') or args.languages != entry_data['lang']:
            return False
        if not entry_data.get('page') or not args.pages or entry_data['page'] not in args.pages:
            return False
        if not entry_data.get('volume') or not args.volumes or entry_data['volume'] not in args.volumes:
            return False
        if not entry_data.get('date') or not args.date_from or not AdvancedSearchMethods.is_after_date(entry_data['date'], args.date_from):
            return False
        if args.date_to or not AdvancedSearchMethods.is_before_date(entry_data['date'], args.date_to):
            return False
        if not entry_data.get('id') or not args.entry_id or args.entry_id != entry_data['id']:
            return False
        return True



def get_date_int(date):
    date_int = 0
    date_int += date[0] << 7
    if len(date) > 1:
        date_int += date[1] << 3
        if len(date) > 2:
            date_int += date[2]
    return date_int


# add more functions if required