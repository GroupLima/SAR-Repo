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

#works
def sort_best_matches(matches):
    sorted_matches = dict(sorted(matches.items(), key=lambda item: (item[1]['accuracy_score'], item[1]['match_frequency']),reverse=True))
    return sorted_matches

#works
def sort_frequency(matches):
    sorted_matches = dict(sorted(matches.items(), key=lambda item: (item[1]['match_frequency'], item[1]['accuracy_score']),reverse=True))
    return sorted_matches

#requires volume and page
def sort_volume_page_ascending(matches):
    pass

#requires volume and page
def sort_volume_page_descending(matches):
    pass

#requires dates
def sort_chronological(matches):
    pass