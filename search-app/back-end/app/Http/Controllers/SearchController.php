<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Http;
use Symfony\Component\Process\Process;
use Illuminate\Support\Facades\Cache;

class SearchController extends Controller
{
  protected $jsonFilePath;
  protected $jsonData;
  // initializes the xml json data and project root path
  public function __construct()
  {
      // Set the path to the JSON file
      $this->jsonFilePath = resource_path('json/entries.json');

      // Load and decode the JSON data
      if (file_exists($this->jsonFilePath)) {
          $this->jsonData = json_decode(file_get_contents($this->jsonFilePath), true);
      } else {
          //echo "empty";
          $this->jsonData = []; // Initialize to an empty array if file does not exist
      }
  }


    /*
    Search Process:

                                        CLIENT SIDE
        html        ->   1. user interface allows users to input in search fields
        vue         ->   2. input is collected from search fields and compiled into a search query. A GET request passes 
                            search query to the backend at route api/search. for xquery, it routes to api/runXQuery
                                        SERVER SIDE
route_controller    ->   5. url request is routed through route controller
route_controller    ->   6. route controller validates request for security
route_controller    ->   7. valid request sent back to search controller
search_controller   ->   8. search controller calls search function and validates parameters and calls
                            relevant python script, passing in the json_data and formatted parameters object
python(xquery)           9. xquery does stuff and returns matches (refer to example of what $matches
                            should look like in function search() in SearchController.php)
python(other search)->  10. if not autocomplete, python filter entries through advanced search to comply
                            with the filters
python(other search)->  11. python searches string matches within filtered entries using python and stores
                            match data in dictionary
python(other search)->  12. python sorts the entries by desired criteria
python              ->  13. python returns results to search controller and stored
search_controller   ->  14. results are limited to results per page, then converted to html, and highlighted
                            where there are matches
search_controller   ->  15. sorted results (html text, other match data, entry data, etc.) are returned and
                            sent back to vue as a json response, completing the async request
                                        CLIENT SIDE
        vue         ->  16. vue gets response with results
        vue         ->  17. vue includes results in relevant views (entries.blade.php, search.blade.php, etc)
    sass+html           18. html and css are applied to style the views



  /*
    XML file naming system:
    ARO-(beginning_volume)-(beginning_page)-(beginning_chapter)_ARO-(ending_volume)-(ending_page)-(ending_chapter).xml

    python functionality:
    2. returns results found for entries:
        a. entry id of each entry
        b. match in each result
    xml filters (queries according to user input):
    1. dates
    2. language (Latin, Scots, Dutch)
    3. Volume
    4. Page
    5. Paragraph
    6. Entry ID
    7. results per page
    8. spelling variants
        a. Use number and description e.g., 1 - One altered character from query, 2
    9. queries matches according to
        a. spelling variants
        b. exact match
        c. phrase
        d. begins with
        e. contains
        f. ends with
 - Two altered characters from query (rephrase)
    */



    protected $match_results = [];

    public function search(Request $request){
        try {
            //get request parameters
            $params = $request->all();
            //convert vue data params to backend params eg. endDate -> end_date
            $permitted = $this->simplify_search_params($params);
            //get search script based on query type eg. xquery, basic_search, advanced_search, autocomplete, autocomplete entry
            $python_search_file = $this->get_search_path($permitted['qt']);
            
            //get matches from any type of search
            $permitted_params = escapeshellarg(json_encode($permitted));
            
            //$command = "python3 $python_search_file_arg $permitted_params";
            $command = "python3 $python_search_file $permitted_params";
            //extracts the json output object
            $raw_output = shell_exec($command);
            $output = json_decode($raw_output, true);
            
            //store matches
            $this->match_results = $output["results"];
            // Check if $this->match_results is not null and is an array
            $total_results = (is_array($this->match_results) && count($this->match_results) > 0) ? count($this->match_results) : 0;

            //format results with convert relevent text to html, add highlights, filter by page, etc
            $display_results = $this->filter_and_format($permitted);
            $num_results = (is_array($display_results) && count($display_results) > 0) ? count($display_results) : 0;
            $variant = $permitted['var'];
            // Return the JSON response with the validated data
            return response()->json([
                'success' => true,
                'num_results' => $num_results,
                'total_results' => $total_results,
                'results' => $display_results,
                'message' => $output['message'],
                'variant' => $variant
            ]);

        } catch (ValidationException $e){
            return response()->json([
                'success' => false,
                'message' => 'Invalid parameters, add an error view instead of this message',
                //route to valid error page eventually
            ]);
        }
    }

    function simplify_search_params($params){
        $permitted = [];
        
        //left is python right is vue (basic search)
        $permitted['query'] = $params['basicSearch'] ?? '';
        $permitted['case_sensitive'] = $params['caseSensitive'] ?? false;
        $permitted['qt'] = $params['query_type'] ?? 'basic_search';
        $permitted['var'] = $params['variant'] ?? 0;
        $permitted['sm'] = $params['methodSearch'] ?? 'word_start';
        $permitted['rpp'] = $params['resultsPerPage'] ?? 5;
        $permitted['pageNo'] = $params['page'];
        $permitted['sort'] = $params['sortBy'];

        // advanced search params (advanced search)
        $permitted['entry_id'] = $params['docId' ?? null];
        $permitted['date_from'] = $params['startDate'] ?? null;
        $permitted['date_to'] = $params['endDate'] ?? null;
        $permitted['vol'] = $params['volumes'] ?? null;
        $permitted['page'] = $params['pageSearch'] ?? null;
        $permitted['lang'] = $params['language'] ?? null;

        return $permitted;
    }


    function get_search_path(){
        return '../resources/python/Search.py';
    }

    function filter_and_format($permitted) {
        
        $query_type = $permitted['qt'];
        $current_page = $permitted['pageNo'];
        $results_per_page = $permitted['rpp'];
        //format the basic/advanced search results
        
        $display_results = [];

        // Check if match_results are available and not empty
        if (empty($this->match_results)) {
            return []; // No results to display
        }
        $start_of_page = ($current_page-1) * $results_per_page;
        // get results from the array of match_results staring at $start_of_page for length of $results_per_page
        $page_results = array_slice($this->match_results, $start_of_page, $results_per_page);
        
        $language_map = [ // better names of languages to be displayed
            'sc' => 'Middle Scots',
            'la' => 'Latin',
            'mul' => 'Multiple'
        ];

        if ($page_results != null){
            foreach ($page_results as $entry_id => $entry) {
                $content = $this->jsonData[$entry_id]['content'];
                $volume = $this->jsonData[$entry_id]['volume'];
                $page = $this->jsonData[$entry_id]['page'];
                $date = $this->jsonData[$entry_id]['date'];
                $language_code = $this->jsonData[$entry_id]['lang'];

                // Map the language code to a full name
                $language_full = $language_map[$language_code] ?? $language_code;

                $htmlcontent = $this->convert_to_html($content);
                
                $matches = $entry['matches'];
                $highlighted_html = $this->highlight($htmlcontent, $matches);

                $display_results[$entry_id] = [
                    'highlighted_html' => $highlighted_html,
                    'volume' => $volume,
                    'page' => $page,
                    'date' => $date,
                    'lang' => $language_full,
                ];
            }
        }
        
        return $display_results;
        //return false if parametters couldnt be applied
    }

    //get chunk of results (if user requested 10 results per page, get the first 10 results)
    function get_results_for_page($rpp){
        //use modulus to determine which chunk of results to return according to rpp (results per page)
        return $rpp;
    }

    function convert_to_html($content){
        $html = htmlspecialchars($content, ENT_QUOTES, 'UTF-8');
        return $html;
    }

    // add highlight tags to content
    function highlight($htmltext, $matches){
        // can highlight either whole word (word start, word middle, word end)
        // or can highlight the specific match
        $opening_tag = '<span class="highlight">';
        $closing_tag = '</span>';
        //$highlighted_htmlcontent = $htmltext;
        foreach ($matches as $match){
            $substring = $match[0];
            //echo $substring . ' ';
            $escaped_text = preg_quote($substring, '/');
            //echo 'escaped text: ' . $escaped_text . ' ';
            //$highlighted_htmlcontent = preg_replace("/($escaped_text)/i", "$opening_tag$1$closing_tag", $highlighted_htmlcontent);
            $pattern = '/\b' . $escaped_text . '\b/';
            $htmltext = preg_replace($pattern, "$opening_tag$substring$closing_tag", $htmltext);

            //echo 'highlights: ' . $htmltext . '; <br>';
        }
        return $htmltext;
    }

    public function getRawEntry(Request $request){
        $entry_id = $request->query('docId');
        if (isset($this->jsonData[$entry_id])){
            return response()->json([
                'success' => true,
                'content' => $this->jsonData[$entry_id]['content'],
                'volume' => $this->jsonData[$entry_id]['volume'],
                'page' => $this->jsonData[$entry_id]['page'],
                'date' => $this->jsonData[$entry_id]['date'],
                'lang' => $this->jsonData[$entry_id]['lang'],
            ]);
        } else {
            return response()->json(['success' => false]);
        }
    }


    public function runXQuery(Request $request)
    {
        // Log or process the received data
        $data = $request->all(); // Get all incoming request data
        $queryType = $data['query_type']; // "xquery" or "xquery_page"
        $queryId = $data['queryId'] ?? null;
        $page = intval($data['page'] ?? 1);
        $pageSize = intval($data['pageSize'] ?? 20);
        
        // If this is a page request for a previous query, check the cache
        if ($queryType === "xquery_page" && $queryId) {
            if (Cache::has("xquery_results_$queryId")) {
                $cachedResults = Cache::get("xquery_results_$queryId");
                // Calculate pagination offsets
                $totalResults = $cachedResults['count'] ?? 0;
                $totalPages = ceil($totalResults / $pageSize);
                
                // Create a paginated response using the cached results
                $paginatedXml = $this->paginateXmlResults($cachedResults['xml'], $page, $pageSize);
                
                return response()->json([
                    'success' => true,
                    'queryResults' => $paginatedXml,
                    'queryId' => $queryId,
                    'totalResults' => $totalResults,
                    'totalPages' => $totalPages
                ]);
            } else {
                return response()->json([
                    'success' => false,
                    'error' => 'Query results no longer in cache. Please run your query again.'
                ], 404);
            }
        }
        
        // For new queries, we need to run the XQuery
        $query = $data['query'] ?? '';
        
        if (empty($query)) {
            return response()->json([
                'success' => false,
                'error' => 'Query cannot be empty'
            ], 400);
        }

        // Generate a new query ID for this request
        $newQueryId = md5($query . time());

        // XQuery to fetch elements from XML files
        $xquery = <<<XQUERY
        xquery version "3.1";
        declare namespace ns = "http://www.tei-c.org/ns/1.0";
        declare option exist:output-size-limit "-1";

        let \$all-items := {$query}
        let \$count := count(\$all-items)
        return
            <results>
                <count>{\$count}</count>
                <items>{\$all-items}</items>
            </results>
        XQUERY;

        // Initialize cURL session
        $ch = curl_init();

        // Set the cURL options for running the XQuery
        curl_setopt($ch, CURLOPT_URL, "http://exist:8080/exist/rest/db/xmlfiles");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
        curl_setopt($ch, CURLOPT_USERPWD, "admin:"); // Basic authentication
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/x-www-form-urlencoded"]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(['_query' => $xquery]));
        curl_setopt($ch, CURLOPT_TIMEOUT, 60); // Set a 60-second timeout

        // Execute the cURL request and get the response
        $response = curl_exec($ch);
        $curlError = curl_error($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($curlError || $httpCode >= 400) {
            return response()->json([
                'success' => false,
                'error' => "XQuery execution failed: $curlError",
                'httpCode' => $httpCode
            ], 500);
        }

        // Cache the full results for future page requests
        Cache::put("xquery_results_$newQueryId", [
            'xml' => $response,
            'count' => $this->extractResultCount($response)
        ], 3600); // Cache for 1 hour

        // Paginate the results for the current request
        $totalResults = $this->extractResultCount($response);
        $totalPages = ceil($totalResults / $pageSize);
        $paginatedResponse = $this->paginateXmlResults($response, $page, $pageSize);
        
        // Return the response
        return response()->json([
            'success' => true,
            'queryResults' => $paginatedResponse,
            'queryId' => $newQueryId,
            'totalResults' => $totalResults,
            'totalPages' => $totalPages
        ]);
    }

    /**
     * Extract the count of results from the XML response
     */
    private function extractResultCount($xmlString) {
        $count = 0;
        try {
            $xml = new \SimpleXMLElement($xmlString);
            $countNode = $xml->count;
            if ($countNode) {
                $count = (int)$countNode;
            }
        } catch (\Exception $e) {
            // In case of XML parsing error, return 0
        }
        return $count;
    }

    /**
     * Paginate XML results for the requested page
     */
    private function paginateXmlResults($xmlString, $page, $pageSize) {
        try {
            $xml = new \SimpleXMLElement($xmlString);
            $doc = new \DOMDocument('1.0', 'UTF-8');
            $doc->formatOutput = true;
            
            // Create a new result structure
            $results = $doc->createElement('results');
            $doc->appendChild($results);
            
            // Add count element
            $count = $doc->createElement('count', (string)$xml->count);
            $results->appendChild($count);
            
            // Create items container
            $items = $doc->createElement('items');
            $results->appendChild($items);
            
            // Calculate pagination offsets
            $totalItems = (int)$xml->count;
            $start = ($page - 1) * $pageSize;
            $end = min($start + $pageSize, $totalItems);
            
            // Get items for current page
            $itemsXml = $xml->items->children();
            $i = 0;
            foreach ($itemsXml as $item) {
                if ($i >= $start && $i < $end) {
                    // Import this node into our new document
                    $importedNode = $doc->importNode(dom_import_simplexml($item), true);
                    $items->appendChild($importedNode);
                }
                $i++;
                // Break early if we've reached our quota
                if ($i >= $end) break;
            }
            
            return $doc->saveXML();
        } catch (\Exception $e) {
            // In case of error, return the original XML
            return $xmlString;
        }
    }
}