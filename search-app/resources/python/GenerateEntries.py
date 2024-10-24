import json
import os.path
import xml.etree.ElementTree as ET 

file_name = 'EntryObjects.json'

class EntryObject():
  # initialise the entry, make params optional to declare
  def __init__(self, id=None, volume=None, page=None, chapter=None, language=None, date=None, type=None, content=None):
    self.id = id
    self.volume = volume
    self.page = page
    self.chapter = chapter
    self.language = language
    self.date = date
    self.type = type
    self.content = content
    
  # return the entry values as dictionary so that they can be looped through  
  def entry_dict(self):
    return {
      'id': self.id,
      'volume': self.volume,
      'page': self.page,
      'chapter' : self.chapter,
      'lang': self.language,
      'date': self.date,
      'type': self.type,
      'content': self.content
    }

class JSONEntries():
  def __init__(self):
    self.volumes1_7path = './xml_files/XML files volumes 1-7'
    self.volume8path = './xml_files/XML files volume 8'
    self.xml_files = []
    self.entry_objects = []
    self.entry_types = ['heading', 'incompleteEntry', 'entry']
    self.json_directory = 'resources/json'
    self.json_filename = 'entries.json'
    self.json_filepath = self.json_directory + self.json_filename

  def add_files(self, path):
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        if os.path.isfile(file):
          self.xml_files.append(file)

  def locate_files(self):
    if os.path.exists(self.volumes1_7path) and os.path.exists(self.volumes1_7path):
      self.add_files(self.volumes1_7path)
      self.add_files(self.volume8path)
    else:
      return None


  def generate_json_object(self):
    try:
      self.locate_files()
      if self.xml_files == []:
        raise FileNotFoundError
      
      entry_objects = []

      for file_path in self.xml_files:
        #create an XMLReader
        tree = ET.parse(file_path)

        #get xml entries
        for item in tree.getroot().findall('./body/div'):
          entry_date = item.find('p/date').attrib.get('when') or None

          for entry in item.findall('div'):
            entry_type = item.attrib.get('type')

            if entry_type in self.entry_types:
              entry_id = item.attrib.get('xml:id'),
              entry_language = item.attrib.get('lang'),
              entry_volume, entry_page, entry_chapter = map(int, entry_id.split('-')[1:])

              entry_content = ''
              content_tags = item.findall('./head|./p')

              if content_tags is not None:
                for tag in content_tags:
                  content += ''.join(tag.itertext())

              entry_obj = EntryObject(
                id = entry_id,
                volume = entry_volume,
                page = entry_page,
                chapter = entry_chapter,
                language = entry_language,
                date = entry_date,
                type = entry_type,
                content = entry_content
              )
              # type="entry" or "heading"
              # xml:id="ARO-1-0001-01"
              # lang="la" (latin)
              # content=""
              entry_objects.append(entry_obj)
              
      #put list of entries inside a json file
      with open(self.json_filepath, 'w'):
        json.dump(entry_objects, self.json_filepath)
              
          
     # with open(file_name, 'w'):
     #     json.dump(entry_objects, file_name)
    except:
      return None


def main():
    #if file already exists, exit program
    print("this python file consists of a json object generator class and an Entry class")
    
    #loop through xml and create an Entry object for each entry. Then store in a list to convert to json?
    pass

if __name__ == "__main__":
  main()