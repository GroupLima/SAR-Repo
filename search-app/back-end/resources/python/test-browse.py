from Search import Search
from pathlib import Path
import sort_methods
import json
from browse_search import BrowseSearch

json_filepath = Path(__file__).resolve().parent.parent / 'json' / 'entries.json'
json_entries = []
with open(json_filepath, 'r') as json_file:
    json_entries = json.load(json_file)


params = {
    'vol': '1'
}


print('searching')
search_obj = BrowseSearch(params, json_entries)
search_obj.start()
matches = search_obj.get_matches()
print('number of entries matched: '+str(len(matches)))
if matches != None:
    json.dumps(matches, indent=4)
    print(json.dumps(matches, indent=4))

    # for page in matches:
    #     for 
        
