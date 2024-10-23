import json
import os.path
import xml.etree.ElementTree as ET 

file_name = 'EntryObjects.json'

class EntryObject():
  # initialise the entry, make params optional to declare
  def __init__(self, entry_id=None, volume=None, page=None, language=None, date=None, content=None):
    self.entry_id = entry_id
    self.volume = volume
    self.page = page
    self.language = language
    self.date = date
    self.content = content
    
  # return the entry values as dictionary so that they can be looped through  
  def entry_dict(self):
    return {
      'entry_id': self.entry_id,
      'volume': self.volume,
      'page': self.page,
      'language': self.language,
      'date': self.date,
      'content': self.content
    }
  

def generate_json_object():
    
    entry_objects = []
    
    #get xml entries

    
    with open(file_name, 'w'):
        json.dump(entry_objects, file_name)

def main():
    #if file already exists, exit program
    #create an XMLReader
    tree = ET.parse(xmlfile)
    
    #loop through xml and create an Entry object for each entry. Then store in a list to convert to json?
    pass

if __name__ == "__main__":
  main()