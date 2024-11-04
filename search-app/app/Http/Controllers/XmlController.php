<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\File;
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
        } else {
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
    public static function get_inner_text($entry){
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
    public static function get_xml_path($entry_id){
        if (isset($jsonData[$entry_id])) {
            $relative_path = $jsonData[$entry_id]['file_path'];
        }
        // error with path, will fix later
        $path = File::path(base_path(), $relative_path);
        
        return $path;
    }

    public static function get_entry($path, $id){
        // load the xml as a simple xml element
        $xml = simplexml_load_file($path);

        // Register the TEI namespace
        $xml->registerXPathNamespace('tei', 'http://www.tei-c.org/ns/1.0');
        
        // get entry where xml:id is $id
        $entry = $xml->xpath("//tei:div[@xml:id='{$id}']");

        // Check if the entry exists
        if (!empty($entry)) {
            return $entry[0]; // Return the first match (or the only match)
        } else {
            return null; // Return null if no entry found
        }

        return $entry;
    }

    // this function returns a filtered list of entries based on params derived from the user's search request
    // when calling this function, assume we've already searched the transcriptions and we have the match results
    // also assume that the entries have been filtered, and all we need to do is find the corresponding xml entries
    public static function get_all_entries($params=null, $match_results=null){
        // if params is null, user has not updated their search and we can fetch recent data
        // use vue to store and retrieve user search history

        $entries = [];

        if ($match_results == null){
            // no entries
            // ...
        }
        else {
            /*
            for each id in results, obtain the filepath where it exists and extract the entry data
                $path = self::get_xml_path();
                $entries .= get_entry($path);
            */
           
        }
        
        // for now, we will only search a test file, but later we'll search all files
        //$test_file = '/Users/caitlin/Documents/GitHub/SAR-Repo/search-app/storage/app/xml-files/XML files volumes 1-7/ARO-1-0001-01_ARO-1-0013-09.xml';
        $test_id = 'ARO-1-0001-02';
        $path = self::get_xml_path($test_id);

        // add new entry to the list
        $entries[] = self::get_entry($path, $test_id);

        return $entries;
    }

    // this function provides entry data for the entries.blade.php view
    public static function display_entries(){
        // assume that the entries returned have been filtered correctly
        $entries = self::get_all_entries();

        // initiate an empty list
        $entry_dicts = [];

        foreach ($entries as $entry){

            // put elements in a dictionary and add dictionary to entries
            $entry_dicts[] = [
                'xml' => nl2br(htmlentities($entry->asXML())),
                'inner_text' => self::get_inner_text($entry),
                
                // use json data or parse xml to get actual values
                // these are just placeholder values for now
                'entry_type' => 'example_type',
                'id' => 'example_id' . sizeof($entry_dicts),
                'volume' => 1,
                'chapter' => 1,
                'page' => 1,
                'date' => '1111-11-11',
                'language' => 'english'
            ];
        }

        return $entry_dicts;

    }

}



