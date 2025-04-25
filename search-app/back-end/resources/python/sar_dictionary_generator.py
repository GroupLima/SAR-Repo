# looks through the entries.json and puts all unique words in a dictionary where each value contains a list of the most likely subsequent words
"""
for each entry, look at the content
add word to dictionary
if next_word exists after word, check if next_word is in word's set,
"""
from pathlib import Path
import os.path
import json

class SarDictionaryGenerator():
    default_dictionary_filepath = Path(__file__).resolve().parent.parent / 'json' / 'sar_dictionary.json'
    default_entries_filepath = Path(__file__).resolve().parent.parent / 'json' / 'entries.json'

    @staticmethod
    def populate_dictionary(entries_file, dictionary_file):
        sar_dictionary = {}

        with open(entrees_file, 'r') as f:
            json_entries = json.load(f)

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
    @staticmethod
    def describe():
        print(f'''
        ******************************************************************************
                            About Sar Dictionary Generator
        ******************************************************************************

        This program generates a dictionary of words and their possible follow-up words from the content of xml entries in entries.json.
        The output is saved in a JSON file named 'sar_dictionary.json'.
        The default write path is ', {SarDictionaryGenerator.default_dictionary_filepath}

        The entries.json file is located by default at {SarDictionaryGenerator.default_entries_filepath}.

        ******************************************************************************
        ''')

    @staticmethod
    #selects json path and creates the file
    def generate_json_dict(entries_file=None, dictionary_file=None):
        try:
            if not entries_file:
                entries_file = SarDictionaryGenerator.default_entries_filepath
            if not dictionary_file:
                dictionary_file = SarDictionaryGenerator.default_dictionary_filepath

            #get the data
            populated_dictionary = SarDictionaryGenerator.populate_dictionary(dictionary_fileh)
            with open(dictionary_file, 'w') as d:
                #print('file exists')
                #print(self.entry_objects)
                json.dump(populated_dictionary, d, indent=4)
                print('\nDictionary data successfully written to ', dictionary_file)
        except FileNotFoundError as e:
            print(f'Error: {e}')
        except Exception as e:
            print(e, '\nwasn\'t able to generate json file')

    def get_filepaths():
        json_entries_file = input('Specify the json path to read entries from (press enter to skip)> ')
        if json_entries_file and not os.path.exists(json_entries_file):
            print('path directory doesn\'t exist'. json_entries_file)
            return False, json_entries_file, None

        dictionary_file = input('Specify the json path (include filename) to write to (press enter to skip)> ')
        if dictionary_file and not dictionary_file.endswith('.json'):
            print("The filename needs to end with \'.json\'.")
            return False, json_entries_file, dictionary_file

        #handles file that already exists at path
        elif os.path.exists(dictionary_file) or (not dictionary_file and os.path.exists(SarDictionaryGenerator.default_dictionary_filepath)):
            overwrite = input('this file already exists, would you like to overwrite it? (y/n)> ')
            if overwrite.strip().lower() == 'y':
                return True, json_entries_file, dictionary_file
            else:
                print('exiting program')
                return False, json_entries_file, dictionary_file
        
        #if directory not found
        elif not os.path.exists(os.path.dirname(dictionary_file)):
            print('directory doesn\'t exist', os.path.dirname(dictionary_file))
            return False, json_entries_file, dictionary_file

        return True, json_entries_file, dictionary_file

def main():
    SarDictionaryGenerator.describe()
    #if file already exists, exit program
    file_exists, entries_file, dictionary_file = SarDictionaryGenerator.get_filepaths()
    if file_exists:
        if not entries_file:
            entries_file == None
        if not dictionary_file:
            print('...\nwriting dictionary data to ', SarDictionaryGenerator.default_dictionary_filepath)
            dictionary_file == None
        else:
            print('...\nwriting dictionary data to ', dictionary_file)
        #generate a dictionary of objects inside a json file
        SarDictionaryGenerator.generate_json_dict(entries_file, dictionary_file)
    


if __name__ == "__main__":
  main()