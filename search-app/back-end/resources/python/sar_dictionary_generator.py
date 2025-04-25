# looks through the entries.json and puts all unique words in a dictionary where each value contains a list of the most likely subsequent words
"""
for each entry, look at the content
add word to dictionary
if next_word exists after word, check if next_word is in word's set,
"""
import json

class SarDictionaryGenerator():
    def generate_sar_dictionary(self, json_entries):
        sar_dictionary = {}
        for entry_id, data in json_entries.items():
            content = data['content']
            words = content.split(" ")
            for i in range(len(words) - 1):
                current_word = words[i].strip(".,!?\\").lower()
                next_word = words[i + 1].strip(".,!?\\").lower() if i + 1 < len(words) else None

                if current_word not in sar_dictionary:
                    sar_dictionary[current_word] = { 'next_words': {}, 'total_count': 1 }
                else:
                    sar_dictionary_count[current_word]['count'] += 1

                #if there is a next_word after current_word, add next_word as a possible follow up word for current_word
                if next_word:
                    next_words_dict = sar_dictionary[word]['next_words']
                    if next_word in next_words_dict:
                        next_words_dict[next_word] += 1
                    next_words_dict[next_word] = 1

        return sar_dictionary
        """
        dictionary structure:
        {
            'holly': {
                'next_words': {
                    'laurencius': 3, #not actual real values #follow_count
                    'primo': 2,
                    'ij': 1,
                    'vxor': 1,
                    ...
                },
                'count': 4 #total number of times this word appears throughout the whole json
            },
            ...
        }
        """