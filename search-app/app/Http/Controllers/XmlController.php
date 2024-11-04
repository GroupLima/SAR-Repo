<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Log;
use Mockery\Generator\StringManipulation\Pass\Pass;
use SebastianBergmann\Type\NullType;

class XmlController extends Controller
{
    protected $jsonFilePath;
    protected $jsonData;

    public function __construct()
    {
        // Set the path to the JSON file
        $this->jsonFilePath = resource_path('json/entries.json');
        
        // Load and decode the JSON data
        if (file_exists($this->jsonFilePath)) {
            $this->jsonData = json_decode(file_get_contents($this->jsonFilePath), true);
            echo "<pre>"; // Optional: Adds HTML formatting for easier reading in the browser
            print_r($this->jsonData['ARO-1-0001-02']['filepath']);
            echo "</pre>";
        } else {
            echo "empty";
            $this->jsonData = []; // Initialize to an empty array if file does not exist
        }
    }

    /* 
    Search Process:
    1. xmlcontroller takes in search parameters
    2. searches ALL the entries using python
    3. python class returns a data structure with info for each entry such as number of matches found, their indexes, etc
    4. query results to display ones that match the filters
    
    XML file naming system: 
    ARO-(beginning_volume)-(beginning_page)-(beginning_chapter)_ARO-(ending_volume)-(ending_page)-(ending_chapter).xml
    
    python functionality:
    2. returns results found for entries:
        a. entry id of each entry
        b. index, length, and spelling variant of each match in each result

    */

    //python functions here
    function search_entries($content){
        // look through every single entry and return matches of every variance
        // loop through all entries and have an array of tags for each entry
        
    }

    /*
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

    //should be called after matches found
    //! WORK IN PROGRESS
    function query_results(Request $filter_args, $results) {
    //handles user params which is a dictionary of filters
        /*ex.  $filter_args = [ 
                        'language' => 'latin',
                        'page' => '5, 18, 9',
                        'paragraph' => None, 
                        etc...
                    ];
        filter_args['language']; will return 'latin'
        */

       
        $params = [
            'date' => get_date($filter_args->input('date')),
            'language' => get_language($filter_args->input('language')),
            'volume' => get_volume($filter_args->input('volume')),
            'page' => get_page($filter_args->input('page')),
            'paragraph' => get_paragraph($filter_args->input('paragraph')),
            'entry_id' => get_entry_id($filter_args->input('entry_id')),
        ];
        // return something

        function get_date($date_param){
            return NAN;
        }

        function get_language($language_param){
            return NAN;
        }

        function get_volume($volume_param){
            return NAN;
        }

        function get_page($page_param){
            return NAN;
        }

        function get_paragraph($paragraph_param){
            return NAN;
        }

        function get_entry_id($entry_id_param){
            return NAN;
        }
    }

    // example of displaying entries in a file

    // this function extracts the actual transcription of an entry and stores it in inner_text
    public function get_inner_text($entry){
        $dom_node = dom_import_simplexml($entry);
        $inner_text = '';

        // $dom_node->childNodes provides a list of direct child nodes of the current entry
        // childNodes is an instance of DOMNodeList class and is an iterable list type
        foreach ($dom_node->childNodes as $child) {

            // add text to inner_text
            $inner_text .= $dom_node->ownerDocument->saveHTML($child);
        }
        return $inner_text;
    }


    // takes an id and uses it to find the corresponding path in the json file
    public function get_xml_path($entry_id){
        if (isset($this->jsonData[$entry_id])) {
            $relative_path = $this->jsonData[$entry_id]['filepath'];
        } else {
            $relative_path = null;
        }
        $path = base_path($relative_path);
        return $path;
    }

    public function get_entry_xml($path, $id){
        // load the xml as a simple xml element
        $xml_file = simplexml_load_file($path);

        // Register the TEI namespace
        $xml_file->registerXPathNamespace('tei', 'http://www.tei-c.org/ns/1.0');
        
        // get entry where xml:id is $id
        $target_xml = $xml_file->xpath("//tei:div[@xml:id='{$id}']");

        // Check if the entry exists
        if (!empty($target_xml)) {
            return $target_xml[0]; // Return the first match (or the only match)
        } else {
            return null; // Return null if no entry found
        }
        echo $target_xml;
        return $target_xml;
    }

    // this function returns a filtered list of entries based on params derived from the user's search request
    // when calling this function, assume we've already searched the transcriptions and we have the match results
    // also assume that the entries have been filtered, and all we need to do is find the corresponding xml entries
    public function get_all_entries($params=null, $match_results=null){
        // if params is null, user has not updated their search and we can fetch recent data
        // use vue to store and retrieve user search history

        $entries_list = [];

        if ($match_results == null){
            // no entries
            // ...
        }
        else {
            foreach ($match_results as $entry_id => $match_data){
                $path = $this->get_xml_path($entry_id);

                // add new entry to the list
                $entries_list[] = [
                    'id' => $entry_id,
                    'xml' => $this->get_entry_xml($path, $entry_id),
                    // add other elements utilizing match data
                    // ...
                ];
            }
        }

        return $entries_list;
    }

    // this function provides entry data for the entries.blade.php view
    public function display_entries(){

        // test data
        $match_results = [
            'ARO-1-0001-01' => null,
            'ARO-1-0001-02' => null,
            'ARO-1-0001-05' => null,
            'ARO-1-0218-01' => null,
            'ARO-7-1053-04' => null,
            'ARO-8-0033-03' => null
        ];

        // assume that the entries returned have been filtered correctly
        $entries_data = $this->get_all_entries($match_results);

        // initiate an empty list
        $entries = [];

        foreach ($entries_data as $entry){

            // put elements in a dictionary and add dictionary to entries
            $entry_dict = [
                'xml' => nl2br(htmlentities($entry['xml']->asXML())),
                'inner_text' => $this->get_inner_text($entry),
                
                // these are just placeholder values for now
                'entry_type' => 'example_type',
                'id' => $entry['id'],
                'volume' => 1,
                'chapter' => 1,
                'page' => 1,
                'date' => '1111-11-11',
                'language' => 'english'

                // do highlighting stuff here as well
            ];

            $entries[] = $entry_dict;
        }

        return $entries;

    }

}



