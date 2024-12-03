import os
import json
import uuid
import traceback
from pathlib import Path
from BaseXClient import BaseXClient
import socketserver
import logging

logging.basicConfig(level=logging.ERROR)

class XQuerySearch:
    def __init__(self):
        try:
            # Initialize BaseX session
            self.session = BaseXClient.Session("localhost", 1984, "admin", "admin")
            self.working_directory = (
                Path(__file__).resolve().parent.parent.parent / Path("storage/app/xml-files")
            )
        except Exception as e:
            logging.error("Unable to connect to BaseX server.", exc_info=True)
            raise e

    def search(self, user_xquery):
        try:
            db_name = f"temp-xquery-db-{uuid.uuid4()}"
            self.session.execute(f"create db {db_name}")

            # Add all XML files to the temporary database
            for root, directories, files in os.walk(self.working_directory):
                for file in files:
                    if file.endswith(".xml"):
                        self.session.execute(f"add to {db_name} {Path(root) / file}")

            # Process and execute the query
            user_xquery = self.clean_query(user_xquery)
            actual_results = self.session.query(user_xquery).execute()

            self.session.execute(f"drop db {db_name}")
            return self.parse_results(actual_results)
        except BaseXClient.Error as e:
            logging.error("Invalid XQuery provided.", exc_info=True)
            raise e
        except Exception as e:
            logging.error("Error during search operation.", exc_info=True)
            raise e

    def clean_query(self, user_xquery):
        namespace = 'declare namespace ns = "http://www.tei-c.org/ns/1.0";'
        return f"""
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

    def parse_results(self, actual_results):
        results_dict = {}
        count_marker = "<--COUNT="
        count_end_marker = "-->"
        count_start = actual_results.find(count_marker) + len(count_marker)
        count_end = actual_results.find(count_end_marker, count_start)
        result_count = int(actual_results[count_start:count_end].strip())

        results_list = actual_results.split("<!--FLAG_ENTRY_ID=")
        for result in results_list[1:]:
            id_part, content = result.split("-->", 1)
            entry_id = id_part.strip()
            results_dict[entry_id] = content.strip()

        return {"count": result_count, "results": results_dict}


class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            data = self.rfile.readline().strip()
            query = json.loads(data.decode())
            xquery_search = XQuerySearch()

            # Perform the search
            results = xquery_search.search(query['xquery'])
            self.wfile.write(json.dumps({"status": "success", "data": results}).encode())
        except Exception as e:
            error_message = f"Error: {e}"
            logging.error(error_message, exc_info=True)
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"Server running on {HOST}:{PORT}")
        server.serve_forever()
