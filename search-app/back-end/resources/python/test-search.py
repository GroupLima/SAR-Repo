import Search
from pathlib import Path
import json

json_filepath = Path(__file__).resolve().parent.parent / 'json' / 'entries.json'
json_entries = []
with open(json_filepath, 'r') as json_file:
    json_entries = json.load(json_file)

# $param_keys = ['json', 'query', 'rpp', 'var', 'ob', 'sm', 'entry_id', 'date_from', 'date_to', 'vol', 'pg', 'pr', 'lang', 'page']

params = {
    'qt' : 'basic_search',
    'query' : 'pre ka',
    'rpp' : 5,
    'var' : 2,
    'sm' : 'starts with' 
}



"""
params = {
    'qt' : 'basic_search',
    'query' : 'collic',
    'rpp' : 5,
    'var' : 4,
    'sm' : 'starts with' 
}
"""
"""
params = {
    'qt' : 'basic_search',
    'query' : 'culum pn',
    'rpp' : 5,
    'var' : 2,
    'sm' : 'starts with' 
}
"""

"""
params = {
    'qt' : 'basic_search',
    'query' : 'aberdeen',
    'rpp' : 5,
    'var' : 3,
    'sm' : 'starts with' 
}
"""

#similarity scale from observations:
# 100=exact, 
# 90=close to exact, 
# 80=still very close, 
# 70=a few characters off, 
# 60=somewhat similar - not that similar, 
# 50=pretty far off (this should be the highest variance)
# 40=completely different

# variance equivalents (for now)
# 1 variance = at least 90 similarity score
# 2 variance = at least 80 similarity score
# 3 variance = at least 70 similarity score
# 4 variance = at least 60 similarity score
# so, converted variance = abs(variance*10 - 100)

print('searching')
search_obj = Search.search(params, json_entries)
matches = search_obj.get_matches()

if matches != None:
    json.dumps(matches, indent=4)

    for entry_id, match_data in matches.items():
        print(entry_id, match_data)