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
    self.working_directory = Path(__file__).resolve().parent.parent.parent / working_directory
    self.results = []
  
  # Conduct XQuery on every XML file
  def search(self, user_xquery):
    try:
      # print("Searching for: " + user_xquery)
      # OS walk not working as expected, need to debug - should be printing names of xml files
      # print(self.working_directory)
      for (root, volume, xml_file) in os.walk(self.working_directory): # Walk through root, volume dirs, and xml files
        for file in xml_file:
          if file.endswith(".xml"): # Simple check to ensure file to be queried is an XML to prevent errors
            # self.session.execute("open " + file) # Use BaseX to open the XML file
            db_name = Path(file).stem # Get file name without .xml for database name
            self.session.execute(f"create db {db_name} {Path(root) / file}") # temp db for each file
            a = self.session.query(user_xquery).execute() # Process query, then execute it on current db
            # print(a)
            self.results.append(a) # Add result of query to list
            self.session.execute(f"drop db {db_name}") # Drop the database
            self.session.execute("close")
    except Exception as e:
      print(e) # Error handling in case of search failure
if __name__ == "__main__":
  xquery = XQuerySearch(str(Path("storage/app/test-xml-files"))) # Allows cross-platform pathing, likely deployed on Linux but development is on Windows/Mac
  xquery.search("for $id in //@xml:id return $id") 
  for result in xquery.results: # Prints query result with formatting
        print(result)  
  
  r"""
  Talk zone here
  
  oki im looking there, storage/app is empty. well, as long as they exist for u
  xml files are in SAR-Repo\search-app\storage\app\test-xml-files\
  uhhhh weird
  I shouldn't need to push or nothing lemme see if u don't have perms
  wonder what happens when i try to run
  gave u perms so u can try from shared terminal ig

  ModuleNotFoundError: No module named 'BaseXClient'
  i can use source?
  ahh I gotta go in the venv, also yeah go in the venv when working from now on with python cus then we can reproduce the same environment in the future
  ok, and then you can write out the steps here so we can share it with the rest
  I think yeah cus your terminal is zsh lemme look for a sec or mby its just the activate

  Assuming working directory is `SAR-Repo` to enter python virtual environment:

    Run it with `.\SAR_Venv\Scripts\activate.ps1` for windows computers using powershell

    It's `source ./SAR-Venv/Scripts/activate` for Mac/Linux with either zsh/bash shell (also supports Fish)
    
    Leave the venv with deactivate

  can't validate zsh but I'll push now so u can try
  actually mby zsh with wsl let's see how bad that is
  next time i come back you will probably have left, so just make sure to push when ur done
  even if the whole code is broken
  alrighty

  uhh
"""