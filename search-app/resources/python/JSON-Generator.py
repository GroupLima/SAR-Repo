import json
import os.path
import xml.etree.ElementTree as ET 
import re
from pathlib import Path

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
      'volume': self.volume,
      'page': self.page,
      'chapter' : self.chapter,
      'lang': self.language,
      'date': self.date,
      'type': self.type,
      'content': self.content
    }

class JSONGenerator():

  volumes1_7path = './xml-files/XML files volumes 1-7' # path to XML file entries volumes 1-7
  volume8path = './xml-files/XML files volume 8'
  json_filepath = Path(__file__).resolve().parent.parent / 'json' / 'entries.json'
  NS = {
      'tei' : 'http://www.tei-c.org/ns/1.0',
      'xml' : 'http://www.w3.org/XML/1998/namespace'
    }
  entry_types = ['heading', 'incompleteEntry', 'entry']
  
  def __init__(self):
    self.xml_files = [] # array of all XML files within every volume
    self.entry_objects = {}
   

  def add_files(self, path):
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        if os.path.isfile(file) and file.lower().endswith('.xml'):
          self.xml_files.append(file)

  
  def populate_entries_array(self):
    print('adding', len(self.xml_files), 'entries')
    if self.xml_files != []:
      for file_path in self.xml_files:
        #create an XMLReader
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        #get xml entries
        item_elements = root.findall('.//tei:body/tei:div', namespaces=JSONGenerator.NS)
        #print('number of elements found', len(item_elements))
        for item in item_elements:

          #set date if date exists
          entry_date = item.find('tei:p/tei:date', namespaces=JSONGenerator.NS)
          entry_date = entry_date.attrib.get('when') if entry_date is not None else None

          #print('date', entry_date)
          entry_elements = item.findall('tei:div', namespaces=JSONGenerator.NS)
          #print('number of entries for this item', len(entry_elements))
          for entry in entry_elements:
            #print('entry',ET.tostring(item, encoding='UTF-8', method='xml'))
            #print()
            
            entry_type = entry.attrib.get('type')
            #print('entry type', entry_type)

            if entry_type in JSONGenerator.entry_types:
              entry_id = entry.attrib.get(f'{{{JSONGenerator.NS["xml"]}}}id')
              #print('entry id', entry_id)
              entry_language = entry.attrib.get(f'{{{JSONGenerator.NS["xml"]}}}lang')
              #first element of id is 'ARO' so can skip
              entry_volume, entry_page, entry_chapter = map(str, entry_id.split('-')[1:])

              entry_content = ''
              content_tags = entry.findall('./tei:p', namespaces=JSONGenerator.NS)
              #print(content_tags)
              if content_tags:
                for tag in content_tags:
                  for element in tag.iter():
                    #print('element', element)
                    #print('element tag', element.tag, '    ', f'{{{self.NS["tei"]}}}lb')
                    # If the element is a <lb> tag, append a space
                    if element.tag == f'{{{self.NS["tei"]}}}lb':
                      #print('found line break tag')
                      entry_content += ' '
                    # For other tags, append the text (if present)
                    elif element.text:
                      entry_content += re.sub(r'\s+', ' ', element.text).strip()
                      #print(re.sub(r'\s+', ' ', element.text).strip(), 'end')
                    # Handle tail text (text outside the element)
                    if element.tail:
                        entry_content += re.sub(r'\s+', ' ', element.tail).strip()

              entry_content = entry_content.strip()

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
              #set id as key
              self.entry_objects[entry_obj.id] = entry_obj.entry_dict()
              #self.entry_objects.append(entry_obj.entry_dict())

  def locate_files(self, volumes1_7path, volume8path):
    if os.path.exists(volumes1_7path) and os.path.exists(volume8path):
      self.add_files(volumes1_7path)
      self.add_files(volume8path)
    else:
      print('path doesn\'t exist')


  def generate_json_entries(self, xml_files_dir=None, json_filepath=None):
    try:
      if xml_files_dir:
        volumes1_7path = xml_files_dir+'/XML files volumes 1-7'
        volume8path = xml_files_dir+'/XML files volume 8'
        #defaults to object attribute if no argument entered
      else:
        volumes1_7path = JSONGenerator.volumes1_7path
        volume8path = JSONGenerator.volume8path

      if not json_filepath:
        json_filepath = JSONGenerator.json_filepath
      
      #print('json filepath', json_filepath)
      #go to xml directory and add files to self.xml_files
      self.locate_files(volumes1_7path, volume8path)

      #make sure that there are existing files within the directory
      if self.xml_files == []:
        #print('xml files empty')
        raise FileNotFoundError
      else:
        #print('populating')
        #if xml files exist and aren't empty, populate self.entry_objects
        self.populate_entries_array()

        
        with open(json_filepath, 'w') as json_file:
          #print('file exists')
          #print(self.entry_objects)
          json.dump(self.entry_objects, json_file, indent=4)
        print('\nentries successfully generated in ', json_filepath)

    except FileNotFoundError as e:
      print(f'Error: {e}')
    except Exception as e:
      print(e, '\nwasn\'t able to generate json file')

  def describe():
    print("\nthis python file generates a json file consisting of entries from xml files")
    print("the default json path is ", JSONGenerator.json_filepath)


def get_filepaths():
  xml_dir = input('\nSpecify the xml directory (press enter to skip)> ')
  if xml_dir and not os.path.exists(xml_dir):
    return False, xml_dir, None
  
  json_file = input('Specify the json path (include filename) to write to (press enter to skip)> ')
  if json_file and not json_file.endswith('.json'):
    print("The filename needs to end with \'.json\'.")
    return False, xml_dir, json_file

  if os.path.exists(json_file) or (not json_file and os.path.exists(JSONGenerator.json_filepath)):
      overwrite = input('this file already exists, would you like to overwrite it? (y/n)> ')
      if overwrite.strip().lower() == 'y':
        return True, xml_dir, json_file
      else:
        print('exiting program')
        return False, xml_dir, json_file
      
  if json_file and not os.path.exists(os.path.dirname(json_file)):
    print('directory doesn\'t exist')
    return False, xml_dir, json_file
  
  return True, xml_dir, json_file
  
def main():
    JSONGenerator.describe()
    #if file already exists, exit program
    file_exists, xml_dir, json_file = get_filepaths()
    if file_exists:
      if xml_dir == '':
        xml_dir == None
      if json_file == '':
        print('...\ngenerating entries at ', JSONGenerator.json_filepath)
        json_file == None
      else:
        print('...\ngenerating entries at ', json_file)
      #loop through xml and create an Entry object for each entry. return a dictionary of objects inside a json file
      generator = JSONGenerator()
      generator.generate_json_entries(xml_dir, json_file)
    


if __name__ == "__main__":
  main()