from pathlib import Path
import os
from BaseXClient import BaseXClient
from pathlib import Path
import time

# Creating session to be able to query XML files - aka database

class XQuerySearch():
  def __init__(self, working_directory):
    # Change standard port for security - also should create encrypred credentials later
    self.session = BaseXClient.Session("localhost", 49888, "admin", "admin")
    self.working_directory = working_directory
    self.working_directory = Path(__file__).resolve().parent.parent.parent / working_directory
    self.results = ()  
  
  # Conduct XQuery on every XML file
  def search(self, user_xquery):
      try:
          db_name = "temp-xquery-db" 
          self.session.execute(f"create db {db_name}")  # Create the database

          for root, directories, files in os.walk(self.working_directory):  # Walk through root, directories, and files
                          for directory in directories:
                              print(f"Discovered directory: {directory}")
                          for file in files:
                              print(f"Discovered file: {file}")
                              print(f"{Path(root) / file}")
                              if file.endswith(".xml"):  # Simple check to ensure file to be queried is an XML to prevent errors
                                  self.session.execute(f"add to {db_name} {Path(root) / file}")  # Add each XML file to the database

          a = self.session.query(user_xquery).execute()  # Process query, then execute it on the database
          self.results += (a,)  # Add result of query to tuple

          self.session.execute(f"drop db {db_name}")  # Drop the database
          self.session.execute("close")
      except Exception as e:
          print(e)  # Error handling in case of search failure  
  
if __name__ == "__main__":
  xquery = XQuerySearch(str(Path("storage/app/test-xml-files"))) # Allows cross-platform pathing, likely deployed on Linux but development is on Windows/Mac
  start_time = time.time()
  xquery.search("for $id in //@xml:id return $id")
  # result_count = 0
  # for result in xquery.results: # Prints query result with formatting
  #   count = len(result.split("\n"))
  #   result_count += count
  print(xquery.results[0])
  elapsed_time = time.time() - start_time
  print(f"Elapsed time: {elapsed_time}")

  # print(f"Total results: {result_count}")
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