import json
import os.path
import xml.etree.ElementTree as ET 
import re

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
    self.volumes1_7path = './xml-files/XML files volumes 1-7' # path to XML file entries volumes 1-7
    self.volume8path = './xml-files/XML files volume 8'
    self.xml_files = [] # array of all XML files within every volume
    self.entry_objects = []
    self.entry_types = ['heading', 'incompleteEntry', 'entry']
    self.json_dir = os.path.join(os.path.dirname(__file__), '..', 'json')
    self.json_filename = 'entries.json'
    self.NS = {
          'tei' : 'http://www.tei-c.org/ns/1.0',
          'xml' : 'http://www.w3.org/XML/1998/namespace'
        }

  def add_files(self, path):
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        if os.path.isfile(file) and file.lower().endswith('.xml'):
          self.xml_files.append(file)

  def locate_files(self):
    print(self.volumes1_7path)
    print(self.volume8path)
    if os.path.exists(self.volumes1_7path) and os.path.exists(self.volume8path):
      self.add_files(self.volumes1_7path)
      self.add_files(self.volume8path)
    else:
      print('path doesn\'t exist')

  def extract_namespace(self, tag):
    if '}' in tag:
      return tag.split('}')[0].strip('{}')
    return ''

  def populate_entries_array(self):
    if self.xml_files != []:
      #print('number of xml files: ', len(self.xml_files))

      for file_path in self.xml_files:
        #print('filepath', file_path)
        #create an XMLReader
        tree = ET.parse(file_path)
        root = tree.getroot()

        tei_namespace = self.extract_namespace(root.tag)
        

        
        #get xml entries
        item_elements = root.findall('.//tei:body/tei:div', namespaces=self.NS)
        #print('number of elements found', len(item_elements))
        for item in item_elements:

          #set date if date exists
          entry_date = item.find('tei:p/tei:date', namespaces=self.NS)
          entry_date = entry_date.attrib.get('when') if entry_date is not None else None

          #print('date', entry_date)
          entry_elements = item.findall('tei:div', namespaces=self.NS)
          #print('number of entries for this item', len(entry_elements))
          for entry in entry_elements:
            #print('entry',ET.tostring(item, encoding='UTF-8', method='xml'))
            #print()
            
            entry_type = entry.attrib.get('type')
            #print('entry type', entry_type)

            if entry_type in self.entry_types:
              entry_id = entry.attrib.get(f'{{{self.NS["xml"]}}}id')
              #print('entry id', entry_id)
              entry_language = entry.attrib.get(f'{{{self.NS["xml"]}}}lang')
              #first element of id is 'ARO' so can skip
              entry_volume, entry_page, entry_chapter = map(str, entry_id.split('-')[1:])

              entry_content = ''
              content_tags = entry.findall('./tei:p', namespaces=self.NS)
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
              #print(entry_obj.content)
              #add dictionary of attributes to self.entry_objects
              self.entry_objects.append(entry_obj.entry_dict())

  def generate_json_file(self, xml_files_dir=None, json_dir=None, json_filename=None):
    try:
      if xml_files_dir:
        self.volumes1_7path = xml_files_dir+'XML files volumes 1-7'
        self.volumes8path = xml_files_dir+'XML files volume 8'
        #defaults to object attribute if no argument entered

      if json_dir:
        self.json_dir = json_dir
        #defaults to object attribute if no argument entered
      
      

      #go to xml directory and add files to self.xml_files
      self.locate_files()

      #make sure that there are existing files within the directory
      if self.xml_files == []:
        #print('xml files empty')
        raise FileNotFoundError
      else:
        #if xml files exist and aren't empty, populate self.entry_objects
        self.populate_entries_array()
        #put list of entries inside a json file
        #print(self.entry_objects)
        #print('finished populating array')
        #print(self.entry_objects)
        json_filepath = os.path.join(json_dir, 'your_file.json')
        with open(self.json_filepath, 'w') as json_file:
          print('file exists')
          json.dump(self.entry_objects, json_file, indent=4)
        print('json file completed')
    except:
      print('wasn\'t able to generate json file')

def create_json_file(xml_files_dir=None, json_dir=None, json_filename=None):
  json_obj = JSONEntries()
  json_obj.generate_json_file(xml_files_dir, json_dir, json_filename)

def main():
    #if file already exists, exit program
    print("this python file consists of a json object generator class and an Entry class")
    create_json_file()
    #loop through xml and create an Entry object for each entry. Then store in a list to convert to json?
    pass

if __name__ == "__main__":
  main()