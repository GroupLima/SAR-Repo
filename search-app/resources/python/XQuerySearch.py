import os, time
from pathlib import Path
from BaseXClient import BaseXClient
from pathlib import Path



class XQuerySearch():
    def __init__(self):
        # Creating session to be able to query XML files - aka database
        # Change standard port for security - also should create encrypred credentials later
        self.session = BaseXClient.Session("localhost", 49888, "admin", "admin")
        self.working_directory = Path(__file__).resolve().parent.parent.parent / Path("storage/app/xml-files")

    # Conduct XQuery on every XML file
    def search(self, user_xquery):
        try:
            db_name = "temp-xquery-db"
            # Create the database
            self.session.execute(f"create db {db_name}")

            # Walk through root, directories, and files
            for root, directories, files in os.walk(self.working_directory):
                # for directory in directories:
                for file in files:
                    # Simple check to ensure file to be queried is an XML to prevent errors
                    if file.endswith(".xml"):
                        # Add each XML file to the database
                        self.session.execute(f"add to {db_name} {Path(root) / file}")

            # Process query, then execute it on the databa
            # Issue is it is returning one massive string
            # I need it in a better data structure format but the limitation of basexclient is that it only returns strings with execute() and there aren't any other ways to parse an XQuery
            # Needed in a dictionary ideally because when it is returned to the frontend it should have it's xml:id attached so that it can immediately link to that entry within the browse section
            user_xquery = self.clean_query(user_xquery)
            actual_results = self.session.query(user_xquery).execute()
            # # Remove carriage return for correct writing to file
            # formatted_results = actual_results.replace("\r", "")
            # # For testing purposes, write to file as terminal has string output limit in VSCode
            # with open(f"./search-app/storage/app/{db_name}_results.txt", "w") as result_file:
                # result_file.write(formatted_results)

            # Drop the database
            self.session.execute(f"drop db {db_name}")
            self.session.execute("close")
            # Return the results in a dictionary format
            return self.parse_results(actual_results)
        except Exception as e:
            print(e)  # Error handling in case of search failure

    def clean_query(self, user_xquery):
        # Clean up the query to ensure it is valid
        # Have to add declaration of namespace in case user doesn't, plus they shouldn't be expected to
        namespace = 'declare namespace ns = "http://www.tei-c.org/ns/1.0";'
        # Flag allows for identifying each entry in the results
        final_xquery = f"""
        {namespace}
        let $results := ({user_xquery})
        let $count := count($results)
        return (
            '<--COUNT=' || $count || '-->',
            for $result in $results
            let $id := $result/@xml:id
            return (
                $result,
                '<!--FLAG_ENTRY_ID=' || $id || '-->'
            )
        )
        """
        return final_xquery

    def count_results(self, results):
        # Count the number of results, +1 because last entry won't have a flag
        if results != {}:
            return results.len()
        return 0

    def parse_results(self, actual_results):
        results_dict = {}
        # Extract the count of results
        count_marker = "<--COUNT="
        count_end_marker = "-->"
        count_start = actual_results.find(count_marker) + len(count_marker)
        count_end = actual_results.find(count_end_marker, count_start)
        result_count = int(actual_results[count_start:count_end].strip())

        # Split the results based on the FLAG_ENTRY_ID marker
        results_list = actual_results.split("<!--FLAG_ENTRY_ID=")
        for result in results_list[1:]:  # Skip the first item as it is the count
            id_part, content = result.split("-->", 1)
            entry_id = id_part.strip()
            results_dict[entry_id] = content.strip()

        return results_dict, result_count


def main():
    # Allows cross-platform pathing, likely deployed on Linux but development is on Windows/Mac
    # xquery = XQuerySearch()
    # user_xquery = 'for $i in //ns:div[@xml:lang="la"] return $i'
    # xquery_results, xquery_count = xquery.search(user_xquery)
    # xquery_count = xquery.count_results()
    # print(xquery_count)
    # for keys, content in xquery_results.items():
    #     print(keys, content)
        # print(xquery_results[keys])
        # print("\n\n\n")
    # print(xquery_results, "\n\n\n")
    # print(xquery_count)

if __name__ == "__main__":
    main()

