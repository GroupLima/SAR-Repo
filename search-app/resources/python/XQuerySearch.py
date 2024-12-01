import time, uuid, os
from pathlib import Path
from BaseXClient import BaseXClient
from pathlib import Path
import xml.sax.saxutils as saxutils

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
            # Also add a unique id
            self.db_name = f"xquery_db-{uuid.uuid4()}"
            # Create the database
            self.session.execute(f"create db {self.db_name}")

            # Walk through root, directories, and files
            for root, directories, files in os.walk(self.working_directory):
                # for directory in directories:
                for file in files:
                    # Simple check to ensure file to be queried is an XML to prevent errors
                    if file.endswith(".xml"):
                        # Add each XML file to the database
                        self.session.execute(f"add to {self.db_name} {Path(root) / file}")

            # Process query, then execute it on the databa
            # Issue is it is returning one massive string
            # I need it in a better data structure format but the limitation of basexclient is that it only returns strings with execute() and there aren't any other ways to parse an XQuery
            # Needed in a dictionary ideally because when it is returned to the frontend it should have it's xml:id attached so that it can immediately link to that entry within the browse section
            actual_results = self.session.query(user_xquery).execute()
            # Remove carriage return for correct writing to file
            formatted_results = actual_results.replace("\r", "")
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
    # Sanitise query to prevent common attacks (e.g., overload server and injection attacks)
    xquery = saxutils.escape(xquery)
    start_time = time.time()
    # Have to add declaration of namespace in case user doesn't, plus they shouldn't be expected to
    namespace = 'declare namespace ns = "http://www.tei-c.org/ns/1.0";'
    # user_xquery = 'for $i in //ns:div[@xml:lang="la"] return $i'
    user_xquery= '''for $div in //ns:div
                    return $div/@xml:id'''
    # Flag allows for identifying each entry in the results
    final_xquery = f"""
    {namespace}
    let $results := ({user_xquery})
    for $result in $results
    return (
        $result,
        '<!--NEW_ENTRY_FLAG-->'
    )
    """
    xquery.search(final_xquery)