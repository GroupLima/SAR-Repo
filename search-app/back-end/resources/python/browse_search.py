import sys
import json
from advanced_search import Advanced_Search
import sort_methods
from errors.custom_errors import BrowseError

from pathlib import Path

class BrowseSearch():

    def __init__(self, params, json_entries=None):
        self.json_entries = json_entries or self.load_json()
        self.params = params

        self.vol = 1
        self.matches = []

    def start(self):
        try:
            self.vol = self.params.get('vol')
            # attempt to convert to integer
            self.vol = [int(self.vol)]

            # use advanced search to get all entries in a single volume
            search_obj = Advanced_Search(None, None, self.vol, None, None, None)
            adv_matches = search_obj.filter_entries(self.json_entries)

            # sort and format results
            grouped_entries = sort_methods.sort_browse_entries_into_list(adv_matches)
            self.matches = self.normalize_attributes(grouped_entries)
        except:
            raise BrowseError(self.vol)

    def load_json(self):
        json_filepath = Path(__file__).resolve().parent.parent / 'json' / 'entries.json'
        with open(json_filepath, 'r') as json_file:
            json_entries = json.load(json_file)
        return json_entries

    def format_date(self, date):
        if date.get("when"):
            return date["when"]
        elif date.get("from") and date.get("to"):
            return f"{date['from']} - {date['to']}"
        elif date.get("from"):
            return f"{datej['from']} -"
        elif date.get("to"):
            return f"- {date['to']}"
        return ''

    def get_full_language(self, lang):
        match lang:
            case 'la': return 'Latin'
            case 'sc' : return 'Middle Scots'
            case 'mul' : return 'Multiple'
            case _: return ''

    def normalize_attributes(self, grouped_entries):
        for page in grouped_entries:
            for entry in page["records"]:
                date = entry.get("date")
                entry["date"] = self.format_date(date)

                lang = entry.get("lang")
                entry["lang"] = self.get_full_language(lang)
        return grouped_entries

    def get_matches(self):
        return self.matches

if __name__ == '__main__':
    if len(sys.argv) > 1:
        permitted = json.loads(sys.argv[1])
        browse_search = BrowseSearch(permitted)
        browse_search.start()
        matches = browse_search.get_matches()
        if matches:
            results = {"message": "matches found", "results": matches}
        else:
            results = {"message": "no matches found", "results": None}
        print(json.dumps(results)) # return the matches data in a JSON object
    else:
        arglen = len(sys.argv)
        results = {"message":  "Not enough arguments. Need parameters.", "results": arglen}
        print(json.dumps(results))
        #print(json.dumps({"error": "Not enough arguments. Need parameters."}))
    