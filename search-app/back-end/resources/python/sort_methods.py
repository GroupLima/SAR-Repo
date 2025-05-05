import re
from advanced_search_methods import AdvancedSearchMethods
"""
return example:
    {
    'ARO-1-0001-03' : {
        'accuracy_score' : value,
        'match_frequency' : value
        'matches' : [
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            ]
        }
    'ARO-1-0001-04' : {
        'accuracy_score' : value,
        'match_freq' : value
        'matches' : [
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            ]
        }
     'ARO-6-0001-01' : {
        'accuracy_score' : value,
        'match_freq' : value
        'matches' : [
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            (string, similarity score, start index),
            ]
        }
    etc...
    }
"""
# considers page numbers with letters as well ex. 130A
def split_page_key(page):
    print(page)
    match = re.match(r'^(\d+)([a-zA-Z]?)$', str(page))
    number = int(match.group(1))
    letter = match.group(2).lower() if match.group(2) else ''
    return (number, letter)

def get_date_from(entry, json_entries):
    date_data = json_entries[entry[0]]['date']
    when = AdvancedSearchMethods.get_date_int_value_or_none(date_data.get('when'))
    if when is not None:
        return when
    from_date = AdvancedSearchMethods.get_date_int_value_or_none(date_data.get('from'))
    return from_date if from_date is not None else float('inf')  # fallback for missing dates

def get_date_to(entry, json_entries):
    date_data = json_entries[entry[0]]['date']
    when = AdvancedSearchMethods.get_date_int_value_or_none(date_data.get('when'))
    if when is not None:
        return when
    from_date = AdvancedSearchMethods.get_date_int_value_or_none(date_data.get('to'))
    return from_date if from_date is not None else 0  # fallback for missing dates

#works descending
def sort_best_matches(matches):
    sorted_matches = sorted(
        matches.items(), 
        key=lambda item: (
            -item[1]['accuracy_score'], 
            -item[1]['match_frequency']
     ))
    return dict(sorted_matches)

#works descending
def sort_frequency(matches):
    sorted_matches = sorted(
        matches.items(), 
        key=lambda item: (
            -item[1]['match_frequency'], 
            -item[1]['accuracy_score']
    ))
    return dict(sorted_matches)

# requires volume and page
# sort matches accprding to their corresponding volume and page in json_entries ascending
def sort_volume_page_asc(matches, json_entries):
    sorted_matches = sorted(
        matches.items(),
        key=lambda item: (
            json_entries[item[0]]['volume'],
            split_page_key(json_entries[item[0]]['page']),
            -item[1]['accuracy_score'],
            -item[1]['match_frequency']
        )
    )
    return dict(sorted_matches)

#requires volume and page
# sort matches accprding to their corresponding volume and page in json_entries descending
def sort_volume_page_dsc(matches, json_entries):
    sorted_matches = sorted(
        matches.items(),
        key=lambda item: (
            int(json_entries[item[0]]['volume']),
            split_page_key(json_entries[item[0]]['page']),
            item[1]['accuracy_score'],
            item[1]['match_frequency']
        ),
        reverse=True
    )
    return dict(sorted_matches)

# requires dates
# sorts matches according to dates from oldest to most recent
def sort_chronological_asc(matches, json_entries):
    sorted_matches = sorted(
        matches.items(),
        key=lambda item: (
            get_date_from(item, json_entries),
            -item[1]['accuracy_score'],
            -item[1]['match_frequency']
        )
    )
    return dict(sorted_matches)

#requires dates
# sorts matches according to dates from most recent to oldest
def sort_chronological_dsc(matches, json_entries):
    sorted_matches = sorted(
        matches.items(),
        key=lambda item: (
            get_date_to(item, json_entries),
            item[1]['accuracy_score'],
            item[1]['match_frequency']
        ),
        reverse=True
    )
    return dict(sorted_matches)

# sort entries into sorted pages
def sort_browse_entries_into_list(json_entries):
    # group into pages
    pages = {}
    for entry in json_entries.values():
        page_name = entry['page']
        if page_name not in pages:
            pages[page_name] = []
        pages[page_name].append(entry)

    # sort the entries within each page
    sorted_pages = sorted(
        pages.items(),
        key=lambda item: (split_page_key(item[0]))
    )

    return [
        {"page": page_name, "records": entries}
        for page_name, entries in sorted_pages
    ]
