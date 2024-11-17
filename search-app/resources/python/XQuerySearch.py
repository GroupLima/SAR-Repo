from pathlib import Path
import os
from BaseXClient import BaseXClient
from pathlib import Path
import time

# Creating session to be able to query XML files - aka database


class XQuerySearch():
    def __init__(self, working_directory):
        # Change standard port for security - also should create encrypred credentials later
        self.session = BaseXClient.Session(
            "localhost", 49888, "admin", "admin")
        self.working_directory = working_directory
        self.working_directory = Path(__file__).resolve(
        ).parent.parent.parent / working_directory
        self.db_name = ""

    # Conduct XQuery on every XML file
    def search(self, user_xquery):
        try:
            self.db_name = "temp-xquery-db"
            # Create the database
            self.session.execute(f"create db {self.db_name}")

            # Walk through root, directories, and files
            for root, directories, files in os.walk(self.working_directory):
                # for directory in directories:
                for file in files:
                    # Simple check to ensure file to be queried is an XML to prevent errors
                    if file.endswith(".xml"):
                        # Add each XML file to the database
                        self.session.execute(f"add to {self.db_name} {
                                             Path(root) / file}")

            # Process query, then execute it on the database
            actual_results = self.session.query(user_xquery).execute()
            print(actual_results)
            formatted_results = actual_results.replace("\n", "") # Remove newlines for correct writing to file
            # For testing purposes, write to file as terminal has string output limit in VSCode
            with open(f"./search-app/storage/app/{self.db_name}_results.txt", "w") as result_file:
                result_file.write(formatted_results)

            # Drop the database
            self.session.execute(f"drop db {self.db_name}")
            self.session.execute("close")
        except Exception as e:
            print(e)  # Error handling in case of search failure


if __name__ == "__main__":
    # Allows cross-platform pathing, likely deployed on Linux but development is on Windows/Mac
    xquery = XQuerySearch(str(Path("storage/app/xml-files")))
    start_time = time.time()
    # Have to add declaration of namespace in case user doesn't, plus they shouldn't be expected to
    namespace = 'declare namespace ns = "http://www.tei-c.org/ns/1.0";'
    xquery.search(namespace + 'for $id in //@xml:id return $id')
    # with open(f"{xquery.db_name}_results.txt", "r") as result_file:
