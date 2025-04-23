<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Http;
use Symfony\Component\Process\Process;


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
        html        ->   1. user interface allows users to input in input fields
        vue         ->   2. vue constantly gets input and stores it in correct data container
        vue         ->   3. for autocomplete, as user is typing, vue automatically collects the stored data
                            in input field and sends an async request to the search controller
        vue         ->   4. for search button, vue collects stored data (already stored in vue) from all
                            relevant input fields and sends an async request to the search controller
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
        // *************BAD PIOTR CODE *******************
        // Log or process the received data
        // echo __DIR__;
        // echo getcwd();

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

        $xquery_doesnt_work = "no";
        if ($xquery_doesnt_work === "xquery") {
            // Do something


            // use the $query to run the xquery python
            //just return results with the query nymber
            // Run the Python script with the escaped query
            //$output = shell_exec($command);
            //echo $output;


            // echo shell_exec('source ../../SAR_Venv/Scripts/activate && echo baba');
            // echo shell_exec('echo $VIRTUAL_ENV');
            //$output = shell_exec('python3 ../resources/python/XQuerySearch.py ');
            //echo exec('basexserver -p49888 -S');
            //sleep(5);
            //echo exec('ss -tuln | grep 49888');
            
            
            #THIS ACTRUALLT MADE IT RUN
            $process = new Process(['python3', '../resources/python/XQuerySearch.py', 'for $i in //ns:div[@xml:lang="la"] return $i']);
            $process->run();
            echo $process->getOutput();
            // Output the result
            if ($process->isSuccessful()) {
                echo $process->getOutput();
            } else {
                echo $process->getErrorOutput();
            }
            
            // $response = Http::post('http://localhost:5000/query', [
            //     'xquery' => 'for $i in //ns:div[@xml:lang="la"] return $i',
            // ]);
            // $result = $response->json();
            
            //sleep
            //echo exec('basexserver -p49888 stop');

            #$output = shell_exec('source ../../SAR-Venv/Scripts/activate && python3 ../../../search-app/resources/python/scuff2.py');
            // $jsonData = json_decode($output, true);
            // echo '$jsonData';
            // echo $output;
            // echo 'so sad';
            //echo $output;


            //$temp = exec('XQuerySearch-SCUFFED.py');
            // $jsonData = json_decode($temp, true);
            //echo($temp);

            // if (json_last_error() === JSON_ERROR_NONE) {
            //     echo $query;
            //     echo "temp: ";
            //     print_r($jsonData);
            //     echo "nothing";
            //     echo " a space";
            // } else {
            //     echo "Error decoding JSON: " . json_last_error_msg();
            // }
         // python3 search-app/resources/python/XQuerySearch.py 'for $i in //ns:div[@xml:lang="la"] return $i'
            // source ./SAR_Venv/Scripts/activate
            // if this fails we need to chmod +x ./SAR_Venv/Scripts/activate (add permission)

            // Decode the JSON output from the Python script
            // $decoded = json_decode($temp, true);

            // if ($decoded) {
            //     // Assign the query results and number of results
            //     $queryResults = $decoded['matches'];
            //     $numberOfXQuery = count($queryResults);

            //     // Example output for debugging
            //     echo "Number of Results: " . $numberOfXQuery . "\n";
            //     echo "Query Results: \n";
            //     print_r($queryResults);  // Or process as needed
            // } else {
            //     echo "Error: No valid JSON returned from Python script.";
            // }
            //$queryResults, $numberOfXQuery = $temp;
            //$queryResults = [
            //     'ARO-8-1290-9' => '<div>working</div>',
            //     'ARO-8-1730-9' => '<div>hello world</div>',
            //     'ARO-8-2989-1' => '<div>hello i like chocolate milk</div>',
            //     'ARO-8-4391-2' => '<div>hi hello implent andreas code here </div>',
            // ];


            // Create a response structure
            //$response = [
            //    'numberOfXQuery' => $numberOfXQuery,
             //   'queryResults' => $queryResults,
            //];
            // Return the response
            //return response()->json(['message' => $response]);
        }else{

            try {
                /*
                // Validate the incoming request
                $validated = $request->validate([
                    //q
                    'basicSearch' => 'required|string|max:255', // Required, must be a string, max length 255
                    //sm
                    'methodSearch' => 'nullable|string|in:keywords,phrase,regularex,word-start,word-middle,word-end', // Optional, must be a valid search method
                    //lang
                    'language' => 'required|string',            // Required, must be a string
                    //var
                    'variant' => 'required|string',             // Required, must be a string
                    //vol
                    'volumes' => 'array',                       // Optional, must be an array
                    //page
                    'pageSearch' => 'nullable|string',          // Optional, must be a string
                    //pr gets every nth entry from every specified page from every specified volume
                    'entrySearch' => 'nullable|string',         // Optional, must be a string
                    //start_date
                    'startDate' => 'nullable|date',             // Optional, must be a valid date
                    //end_data
                    'endDate' => 'nullable|date',               // Optional, must be a valid date
                    //entry_id
                    'docId' => 'nullable|string',               // Optional, must be a string

                    //still need the following data:
                    //rpp (results per page)
                    //ob (order by criteria)
                ]);

                */
                

            } catch (ValidationException $e){
                return response()->json([
                    'success' => false,
                    'message' => 'Invalid parameters, add an error view instead of this message',
                    //route to valid error page eventually
                ]);
            }
        }
        /*
        an example of what $matches looks like:
        {
        'ARO-1-0001-03' : {
            'accuracy_score' : value,
            'match_frequency' : value
            'matches' : [
                (string, similarity score, start index),
                (string, similarity score, start index),
                (string, similarity score, start index),
                (string, similarity score, start index),
                (string, similarity score, start index),
                ]
            }
        'ARO-1-0001-04' : {
            'accuracy_score' : value,
            'match_freq' : value
            'matches' : [
                (string, similarity score, start index),
                (string, similarity score, start index),
                (string, similarity score, start index),
                (string, similarity score, start index),
                (string, similarity score, start index),
                ]
            }
        'ARO-6-0001-01' : {
            'accuracy_score' : value,
            'match_freq' : value
            'matches' : [
                (string, similarity score, start index),
                (string, similarity score, start index),
                (string, similarity score, start index),
                (string, similarity score, start index),
                (string, similarity score, start index),
                ]
            }
        etc...
        }
        */
    }


    public function runXQuery(Request $request)
    {
        // Log or process the received data
        $data = $request->all(); // Get all incoming request data


        //print_r("\n");
        //print_r($data.query.type);
        //print_r($data.query.type);
        $queryType = $data['query_type']; // "xquery"
        $query = $data['query'];         // "hello cait"

        //print_r($queryType);
        //print_r($query);  
        if ($queryType === "xquery") {
            // Do something
            $queryResults = [
                'ARO-8-1290-9' => '<div>working</div>',
                'ARO-8-1730-9' => '<div>hello world</div>',
                'ARO-8-2989-1' => '<div>hello i like chocolate milk</div>',
                'ARO-8-4391-2' => '<div>hi hello</div>',
            ];
        }else{
            $queryResults = [
            'ARO-8-1290-9' => '<div>i want to cry this isnt xquery  </div>',
            'ARO-8-1730-9' => '<div>we we we </div>',
            ];
        }
       

        error_log( 'Hello');
        // XQuery to fetch <item> elements from XML files in the collection

        //$xquery = 'declare namespace ns = "http://www.tei-c.org/ns/1.0"; for $i in //ns:div[@xml:lang="la"] return $i';
        //$query = '//ns:div[@xml:lang="la"]';

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
        curl_setopt($ch, CURLOPT_URL, "http://localhost:8080/exist/rest/db/xmlfiles");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
        curl_setopt($ch, CURLOPT_USERPWD, "admin:"); // Basic authentication
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/x-www-form-urlencoded"]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(['_query' => $xquery]));

        // Execute the cURL request and get the response
        $response = curl_exec($ch);
        
        // Check for errors
        //if(curl_errno($ch)) {
        //    error_log('Errorrrrrrrr:' . curl_error($ch));
        //} else {
        //    error_log('Responceeeeee:' . $response); // Print the query result
        //}


        // // Create a response structure
    
        $response = [
            'queryResults' => $response,
        ];

        // Return the response
        return response()->json(['message' => $response]);
    }

    public function runBasic(Request $request)
    {
        // Log or process the received data
        $data = $request->all(); // Get all incoming request data
       // \Log::info('Received data:', $data);
        //echo $data;
        //print_r("\n");
        //print_r($data.query.type);
        //print_r($data.query.type);
        $queryType     = $data['query_type'];
        $basicSearch   = $data['basicSearch'];
        $methodSearch  = $data['methodSearch'];
        $language      = $data['language'];
        $variant       = $data['variant'];
        $volumes       = $data['volumes'];
        $pageSearch    = $data['pageSearch'];
        $entrySearch   = $data['entrySearch'];
        $startDate     = $data['startDate'];
        $endDate       = $data['endDate'];
        $docId         = $data['docId'];
        echo "\nqueryType";
        echo $queryType;
        echo "\nbasicSearch";
        echo $basicSearch;
        echo "\nmethodSearch";
        echo $methodSearch;
        echo "\nlanguage";
        echo $language;
        echo "\nvariant";
        echo $variant;
        echo "\nvolumes";
        echo $volumes;
        echo "\npageSearch";
        echo $entrySearch;
        echo "\nentrySearch";
        echo $entrySearch;
        echo "\nstartDate";
        echo $startDate;
        echo "\nendDate";
        echo $endDate;
        echo "\ndocId";
        echo $docId;
        echo "\n";
   
        
        if ($queryType === "xquery") {
            // Do somethin
            $queryResults = [
                'ARO-8-1290-9' => '<div>working</div>',
                'ARO-8-1730-9' => '<div>hello world</div>',
                'ARO-8-2989-1' => '<div>hello i like chocolate milk</div>',
                'ARO-8-4391-2' => '<div>hi hello</div>',
            ];
        }else{
            $queryResults = [
            'ARO-8-1290-9' => '<div>ha ha ha caitlin</div>',
            'ARO-8-1730-9' => '<div>we we we </div>',
            ];
        }
        // Define your query results (replace with actual logic as needed)

        // Calculate the number of results dynamically
         $numberOfXQuery = count($queryResults);

        // // Create a response structure
         $response = [
             'numberOfXQuery' => $numberOfXQuery,
             'queryResults' => $queryResults,
         ];

        // Return the response
        return response()->json(['message' => $response]);
    }







    function simplify_search_params($params){

        //params: query_type, user query, results per page, variance, order by asce/desc, search method, entry id, date from, date to, volume, page, paragraph, language, page number
        $param_keys = ['qt', 'query', 'rpp', 'var', 'ob', 'sm', 'entry_id', 'date_from', 'date_to', 'vol', 'page', 'pr', 'lang', 'page'];

        $permitted = [];

        /*

        for basic search example, we need:

            1. (qt) query type: 'basic_search'
            2. (query) query
            3. (var) variance
            4. (sm) search method: 'start with'
            5. (rpp) results per page
        
        */ //left is python right is vue
        $permitted['query'] = $params['basicSearch'] ?? '';
        $permitted['qt'] = $params['query_type'] ?? 'basic_search';
        $permitted['var'] = $params['variant'] ?? 0;
        $permitted['sm'] = $params['methodSearch'] ?? 'word_start';
        $permitted['rpp'] = $params['resultsPerPage'] ?? 5;

        // advanced search params
        $permitted['entry_id'] = $params['docId' ?? null];
        $permitted['date_from'] = $params['startDate'] ?? null;
        $permitted['date_to'] = $params['endDate'] ?? null;
        $permitted['vol'] = $params['volumes'] ?? null;
        $permitted['page'] = $params['pageSearch'] ?? null;
        $permitted['lang'] = $params['language'] ?? null;
        
        //create permitted list of valid parameters relevent to the type of search the user is making
        // foreach ($param_keys as $param){
        //     if (isset($params[$param])) {
        //         $permitted[$param] = $params[$param];
        //     }
        // }
        return $permitted;
    }


    function get_search_path($query_type){
        //$query_type = $permitted['qt'];
        if (strtolower($query_type) == 'xquery'){
            //hardcoded for now
            return '../resources/python/XQuerySearch.py';
        } else {
            return '../resources/python/Search.py' ;
        }
    }

    function filter_and_format($permitted) {

        $query_type = $permitted['qt'];
        $current_page = 1;
        $results_per_page = $permitted['rpp'];

        if (strtolower($query_type) == 'xquery'){
            // display dict_of_results.items() display the data values, have the keys as a tag on the divs of the displayed result chunks

            //store tag and match pairs in $xquery_matches
            $xquery_matches = [];

            $result_dict = $this->match_results[0];

            //not needed? needed because previous team returned number of tresults too
            $num_results = $this->match_results[1];

            foreach ($result_dict as $tag => $content)
            {
                $xquery_matches[$tag] = $content;
            }
            /*
                xquery return example:
                {
                    {'tag' = 'ARO-8-1290-9', 'content' = '<div>hello</div>'},
                    {'tag' = 'ARO-8-1730-9', 'content' = '<div>hello world</div>'},
                    {'tag' = 'ARO-8-2989-1', 'content' = '<div>hello i like chocolate milk</div>'},
                    {'tag' = 'ARO-8-4391-2', 'content' = '<div>hi hello</div>'},
                }
            */
            //set $match_results to new dictionary format
            $this->match_results = $xquery_matches;
        }
        

        //if not autocomplete, highlight the html
        elseif (strpos($query_type, 'autocomplete') !== false ){
            return $this->match_results;
        }

        else {
            //format the basic/advanced search results
            
            $display_results = [];

            // Check if match_results are available and not empty
            if (empty($this->match_results)) {
                return []; // No results to display
            }
            
            uasort($this->match_results, function($a, $b) {
                if ($a['accuracy_score'] == $b['accuracy_score']) {
                    // If accuracy is the same, compare by match_frequency
                    return $b['match_frequency'] - $a['match_frequency']; // Highest frequency first
                }
                return $b['accuracy_score'] - $a['accuracy_score']; // Highest accuracy first
            });
            
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
                    $htmlvolume = $this->convert_to_html($volume);
                    $htmlpage = $this->convert_to_html($page);
                    $htmldate = $this->convert_to_html($date);
                    $htmllang = $this->convert_to_html($language_full);
                    
                    $matches = $entry['matches'];
                    $highlighted_html = $this->highlight($htmlcontent, $matches);
                    $display_results[$entry_id] = [
                        'highlighted_html' => $highlighted_html,
                        'volume' => $htmlvolume,
                        'page' => $htmlpage,
                        'date' => $htmldate,
                        'lang' => $htmllang,
                    ];
                }
            }
            
            return $display_results;
        }
        



        //return false if parametters couldnt be applied
    }

    //get chunk of results (if user requested 10 results per page, get the first 10 results)
    function get_results_for_page($rpp, $page){
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
            $pattern = '/\b' . $escaped_text . '\b/i';
            $htmltext = preg_replace($pattern, "$opening_tag$substring$closing_tag", $htmltext);

            //echo 'highlights: ' . $htmltext . '; <br>';
        }
        return $htmltext;
    }

}