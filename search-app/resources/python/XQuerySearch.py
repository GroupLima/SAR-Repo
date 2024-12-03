try:
    import os
    import sys
    import uuid
    import json
    import traceback
    import logging
    from pathlib import Path
    from BaseXClient import BaseXClient

    class XQuerySearch:
        def __init__(self):
            try:
                # Creating session to be able to query XML files - aka database
                # Change standard port for security - also should create encrypted credentials later
                self.session = BaseXClient.Session("localhost", 49888, "admin", "admin")
                self.working_directory = Path(__file__).resolve().parent.parent.parent / Path("storage/app/xml-files")
            except Exception as e:
                print(f"Error: Unable to connect to BaseX server. Ensure the server is running. {e}")
                raise e

        # Conduct XQuery on every XML file
        def search(self, user_xquery):
            try:
                # Create a unique database name to prevent conflicts with other users
                db_name = "temp-xquery-db" + str(uuid.uuid4())
                # Create the database
                self.session.execute(f"create db {db_name}")

                # Walk through root, directories, and files
                for root, directories, files in os.walk(self.working_directory):
                    for file in files:
                        # Simple check to ensure file to be queried is an XML to prevent errors
                        if file.endswith(".xml"):
                            # Add each XML file to the database
                            self.session.execute(f"add to {db_name} {Path(root) / file}")

                # Process query, then execute it on the database
                user_xquery = self.clean_query(user_xquery)
                actual_results = self.session.query(user_xquery).execute()

                # Drop the database
                self.session.execute(f"drop db {db_name}")
                self.session.execute("close")

                # Return the results in a dictionary format
                return self.parse_results(actual_results)
            except BaseXClient.Error as e:
                print(f"Error: Invalid XQuery provided. {e}") # Error handling in case of invalid XQuery
                raise e
            except Exception as e:
                print('is it this'+str(e))  # Error handling in case of search failure
                raise e

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
        # logging.basicConfig(level=logging.ERROR)  # Set the logging level
        # if len(sys.argv) < 2:
        #     print("Please provide an XQuery to search for.")
        #     sys.exit(1)

        # user_xquery = sys.argv[1]
        # user_xquery = 'for $i in //ns:div[@xml:lang="la"] return $i'
        # user_xquery = 'for $i in //ns:div[@xml:lang="sc"] return $i'
        # user_xquery = 'for $i in //ns:div[@xml:lang="la"] where $i/ancestor::ns:div//ns:date[@when="1501-10-20"] return $i'
        user_xquery = 'for $i in //ns:div[@xml:lang="sc"] where $i/ancestor::ns:div//ns:date[@when >"1501-1-1"][@when <"1502-12-31"] return $i'
        try:
            xquery = XQuerySearch()
            results = xquery.search(user_xquery)
            # print(json.dumps(results))
            print(results[0])
            print(f"Number of results: {results[1]}")
        except Exception as e:
            # Get a full traceback for detailed context
            tb = traceback.format_exc()
            logging.error("An error occurred: ", exc_info=True)
            print(f"An error occurred: {e.__class__.__name__}: {e}")
            print(f"Traceback:\n{tb}")
            sys.exit(1)


    if __name__ == "__main__":
        main()


except ImportError as e:
    print(f"Import Error: {e}")
