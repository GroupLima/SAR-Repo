<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;
use Illuminate\Support\Facades\Log;

class SearchController extends Controller
{
  protected $jsonFilePath;
  protected $jsonData;

  // initializes the xml controller
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
  
    function search(Request $request){
        // *************BAD PIOTR CODE *******************
        // Log or process the received data
        $data = $request->all(); // Get all incoming request data
        \Log::info('Received data:', $data);

        $queryType = $data['query_type']; // "xquery"
        $query = $data['query'];         // "hello cait"
        
        if ($queryType === "xquery") {
            // Do something
            $queryResults = [
                'ARO-8-1290-9' => '<div>working</div>',
                'ARO-8-1730-9' => '<div>hello world</div>',
                'ARO-8-2989-1' => '<div>hello i like chocolate milk</div>',
                'ARO-8-4391-2' => '<div>hi hello implent andreas code here </div>',
            ];

            $numberOfXQuery = count($queryResults);

            // Create a response structure
            $response = [
                'numberOfXQuery' => $numberOfXQuery,
                'queryResults' => $queryResults,
            ];
            // Return the response
            return response()->json(['message' => $response]);
        //********** BAD PIOTR CODE ********************* */
        }else{

            try {
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
                //get request parameters
                $params = $request->query();
                

                //convert vue data params to backend params eg. endDate -> end_date
                $permitted = $this->simplify_search_params($params);

                $permitted['query'] = 'for $i in //ns:div[@xml:lang="la"] return $i'; //put query here
                //get search script based on query type eg. xquery, basic_search, advanced_search, autocomplete, autocomplete entry
                $python_search_file = $this->get_search_path($permitted) . $permitted;


                //get matches from any type of search
                $matches = shell_exec('python3 ' . $python_search_file);

            //     if (strpos($python_search_file, 'XQuerySearch.py') !== false) {
            //     $additional_argument = escapeshellarg(json_encode($permitted)); // Pass parameters as JSON
            //     $command .= ' ' . $additional_argument;
            // }

                //store matches
                $this->match_results = $matches;

                //format results with convert relevent text to html, add highlights, filter by page, etc
                $display_results = $this->filter_and_format($permitted);

                // Return the JSON response with the validated data
                return response()->json([
                    'success' => true,
                    'data' => $display_results,
                ]);
            
            
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
        \Log::info('Received data:', $data);
        
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
            'ARO-8-1290-9' => '<div>i want to cry</div>',
            'ARO-8-1730-9' => '<div>we we we </div>',
            ];
        }
        // Define your query results (replace with actual logic as needed)

        // Calculate the number of results dynamically
        $numberOfXQuery = count($queryResults);

        // Create a response structure
        $response = [
            'numberOfXQuery' => $numberOfXQuery,
            'queryResults' => $queryResults,
        ];

        // Return the response
        return response()->json(['message' => $response]);
    }

    




    

    function simplify_search_params($params){

        //params: query_type, user query, results per page, variance, order by asce/desc, search method, entry id, date from, date to, volume, page, paragraph, language, page number
        $param_keys = ['qt', 'query', 'rpp', 'var', 'ob', 'sm', 'entry_id', 'date_from', 'date_to', 'vol', 'pg', 'pr', 'lang', 'page'];
        
        $permitted = [];

        /*

        for basic search example, we need:

            1. (qt) query type: 'basic_search'
            2. (query) query
            3. (var) variance
            4. (sm) search method: 'start with'
            5. (rpp) results per page

        */
        //create permitted list of valid parameters relevent to the type of search the user is making
        foreach ($param_keys as $param){
            if (isset($params[$param])) {
                $permitted[$param] = $params[$param];
            }
        }
        return $permitted;
    }


    function get_search_path($params){
        $query_type = $params['qt'];
        if (strtolower($query_type) == 'xquery'){
            //hardcoded for now
            return './search-app/resources/python/XQuerySearch.py '; 
        } else {
            return './search-app/resources/python/Search.py ' ;
        }
    }

    function filter_and_format($permitted) {
        //get results to display
        $this->get_results_for_page($permitted['rpp'], 0);

        $query_type = $permitted['qt'];

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
        /*
        
        foreach ($results as &result) {
            if (isset($result->text) && isset($result->matches)){
                //convert to html
            }
        }
        */

        //if not autocomplete, highlight the html
        if (strpos($query_type, 'autocomplete') !== false ){
            return $this->match_results;
        }
        
        

        //return false if parametters couldnt be applied
    }

    //get chunk of results (if user requested 10 results per page, get the first 10 results)
    function get_results_for_page($rpp, $page){
        //use modulus to determine which chunk of results to return according to rpp (results per page)
        return null;
    }

    function convert_to_html($content){
        $html = htmlspecialchars($content, ENT_QUOTES, 'UTF-8');
        return $html;
    }

    // add highlight tags to content
    function highlight($text, $matches){
        // can highlight either whole word (word start, word middle, word end)
        // or can highlight the specific match
        $opening_tag = '<strong>';
        $closing_tag = '</strong>';
        foreach ($matches as $match){
            $escaped_text = preg_quote($match, '/');
            $highlighted_content = preg_replace("/($escaped_text)/i", "$opening_tag$1$closing_tag", $text);
        }
        return $highlighted_content;
    }

}

