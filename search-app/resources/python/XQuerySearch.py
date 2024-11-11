from pathlib import Path
import os
from BaseXClient import BaseXClient
from pathlib import Path

# Creating session to be able to query XML files - aka database

class XQuerySearch():
  def __init__(self, working_directory):
    # Change standard port for security - also should create encrypred credentials later
    self.session = BaseXClient.Session("localhost", 49888, "admin", "admin")
    self.working_directory = working_directory
    self.results = []
  
  # Conduct XQuery on every XML file
  def search(self, user_xquery):
    try:
      print("Searching for: " + user_xquery)
      for root, volume, xml_file in os.walk(self.working_directory): # Walk through root, volume dirs, and xml files
        print(xml_file)
        for file in xml_file:
          if file.endswith(".xml"): # Simple check to ensure file to be queried is an XML to prevent errors
            self.session.execute("open " + file) # Use BaseX to open the XML file
            self.results.append(self.session.execute(user_xquery)) # Add result of query to list
            self.session.execute("close")
    except BaseXClient.SessionException as e:
      print(e) # Error handling in case of search failure
      
if __name__ == "__main__":
  xquery = XQuerySearch(str(Path("storage/xml-files-test"))) # Allows cross-platform pathing, likely deployed on Linux but development is on Windows/Mac
  xquery.search("for $id in //@xml:id return $id/string()")
  print(xquery.results)