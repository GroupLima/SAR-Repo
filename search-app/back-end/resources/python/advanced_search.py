import re
from data_models.model_advanced import AdvancedSearchModel
from advanced_search_methods import AdvancedSearchMethods

""" This class is executes the Advanced Search Filters for Entry ID, Language, Date, Volume and Page. """

class Advanced_Search():
    def __init__(self, language, pages, volumes, entry_id, date_from, date_to):
        self.language = language # input parameters from the user query
        self.pages = pages
        self.volumes = volumes
        self.entry_id = entry_id
        self.date_from = date_from
        self.date_to = date_to

    # filter values of the json entries that match the param values
    def filter_entries(self, json_entries):
        args = AdvancedSearchModel( # format/parse and validate the input parameters
            language = self.language,
            pages = self.pages, 
            volumes = self.volumes, 
            entry_id = self.entry_id,
            date_from = self.date_from, 
            date_to = self.date_to
        )

        # loop through all json entries
        valid_entries = {}
        for entry_id, entry_data in json_entries.items():
            print('is entry')
            if self.is_valid_entry(args, entry_data):
                
                valid_entries[entry_id] = entry_data
        
        return valid_entries
    
    def is_valid_entry(self, args, entry_data):
        # check whether the given input arguments match the entry attributes
        if args.language: 
            if not entry_data.get('lang') and args.language != entry_data['lang']:
                return False #hmohhhoops sorryyyyyy
        print('valid language')
        if args.pages:
            if not entry_data.get('page') or entry_data['page'] not in args.pages:
                return False
        print('valid pages')
        if args.volumes:
            print('volumes detected', entry_data['volume'])
            if not entry_data.get('volume') or int(entry_data['volume']) not in args.volumes:
                print('not valid vol' + entry_data['volume'])
                return False
        print('valid volums')
        if args.date_from:
            if not entry_data.get('date') or not AdvancedSearchMethods.is_after_date(entry_data['date'], args.date_from):
                return False
        print('valid date from')
        if args.date_to and not AdvancedSearchMethods.is_before_date(entry_data['date'], args.date_to):
            return False
        print('valid date to')
        if args.entry_id:
            if not entry_data.get('id') or args.entry_id != entry_data['id']:
                return False
        print('valid entry')
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