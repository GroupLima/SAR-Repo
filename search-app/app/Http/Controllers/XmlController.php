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

    // passes entries to the entries.blade.php view and displays home.blade.php
    public function display_entries($entries){
        // returns all entries
        return view('home', compact('entries'));
    }

    // implement function to display entries on a certain page (when there are too many entries to fit onto one page)
    // other functions ...


    // this function returns a filtered list of entries based on params derived from the user's search request
    // when calling this function, assume we've already searched the transcriptions and we have the match results
    // also assume that the entries have been filtered, and all we need to do is find the corresponding xml entries
    // this function provides entry data for the entries.blade.php view
    public function get_all_entries($params=null){
        // if params is null, user has not updated their search and we can fetch recent data
        // use vue to store and retrieve user search history
        $match_results = $this->get_match_results();

        $entries_list = [];

        if ($match_results == null){
            // no entries
            // ...
        }
        else {
            foreach ($match_results as $entry_id => $match_data){
                $json_data = $this->get_json_entry_data($entry_id);
                $xml_path = $this->get_xml_path($entry_id, $json_data);

                // get all the values
                $id = $entry_id;
                $xml = $this->get_entry_xml($entry_id, $xml_path);
                $inner_text = $this->get_inner_text($xml);
                $volume = $this->get_entry_element('volume', $json_data);
                $chapter = $this->get_entry_element('chapter', $json_data);
                $page = $this->get_entry_element('page', $json_data);
                $date = $this->get_entry_element('date', $json_data);
                $type = $this->get_entry_element('type', $json_data);
                $language = $this->get_entry_element('lang', $json_data);
                // put values inside a dictionary and add the dictionary to entries_list
                $entries[] = [
                    'id' => $id,
                    'xml' => nl2br(htmlentities($xml->asXML())),
                    'inner_text' => $inner_text,
                    'id' => $id,
                    'volume' => $volume,
                    'chapter' => $chapter,
                    'page' => $page,
                    'date' => $date,
                    'type' => $type,
                    'language' => $language
                ];
            }
        }
        //echo 'entries found' . sizeof($entries);
        return $entries;
    }


    // get the json data of a specific entry
    public function get_json_entry_data($entry_id){
        if (isset($this->jsonData[$entry_id])) {
            $data= $this->jsonData[$entry_id];
        } else {
            $data = null;
        };
        return $data;
    }


    // takes an id and uses it to find the corresponding path in the json file
    public function get_entry_element($tag, $data=null, $entry_id=null){
        if ($data != null){
            if (isset($data[$tag])){
                $element = $data[$tag];
            } else {
                $element = null;
            }
        }
        else {
            if (isset($this->jsonData[$entry_id][$tag])) {
                $element = $this->jsonData[$entry_id][$tag];
            } else {
                $element = null;
            }
        }
        return $element;
    }


    // get the file where a specific entry exists
    public function get_xml_path($entry_id, $json_data=null){
        if ($json_data != null){
            $relative_path = $json_data['xmlpath'];
        } else {
            $relative_path = $this->get_entry_element('xmlpath', null, $entry_id)['xmlpath'];
        }
        $path = base_path($relative_path);
        return $path;
    }


    public function get_entry_xml($entry_id, $path){
        // load the xml as a simple xml element
        $xml_file = simplexml_load_file($path);

        // Register the TEI namespace
        $xml_file->registerXPathNamespace('tei', 'http://www.tei-c.org/ns/1.0');

        // get entry where xml:id is $id
        $target_xml = $xml_file->xpath("//tei:div[@xml:id='{$entry_id}']");

        // Check if the entry exists
        if (!empty($target_xml)) {
            return $target_xml[0]; // Return the first match (or the only match)
        } else {
            return null; // Return null if no entry found
        }
        return $target_xml;
    }


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


    public function get_match_results(){

        // search and query
        // ...

        // test data, all results are null for now
        $match_results = [
            'ARO-1-0001-01' => null,
            'ARO-1-0001-02' => null,
            'ARO-1-0001-05' => null,
            'ARO-1-0218-01' => null,
            'ARO-7-1053-04' => null,
            'ARO-8-0033-03' => null,
            'ARO-8-1212-02' => null
        ];

        // match_results will most likely be an object variable

        return $match_results;
    }


}



