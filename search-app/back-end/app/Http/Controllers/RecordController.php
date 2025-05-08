<?php

namespace App\Http\Controllers;

use Illuminate\Validation\ValidationException;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;



class RecordController extends Controller
{
    protected $TEI_namespace;

    public function __construct()
    {
        // register TEI namespace for accessing xml files
        $this->TEI_namespace = 'http://www.tei-c.org/ns/1.0';

    }

    public function getRecords(Request $request)
    {
        try {
            $volume = $request->query('volume');
            // convert from front end to back end naming conventions
            $permitted = [];
            $permitted['vol'] = $volume ?? null;

            // if data already loaded on server, return the data
            if (Cache::has("preload_volume_{$volume}")) {
                return response()->json(Cache::get("preload_volume_{$volume}"));
            } else {
                Log::info('Error fetching preloaded data: ');
            }
            
            // otherwise, try to load the records
            $results_array = $this->loadRecords($volume);
            //$echo $match_results;

            // Return the JSON response with the validated data
            return response()->json($results_array);

        } catch (ValidationException $e){
            return response()->json([
                'success' => false,
                'message' => 'Invalid parameters for browse search',
                //route to valid error page eventually
            ]);
        }
    }

    public function loadRecords($volume) {
        try {
            $permitted['vol'] = $volume;
            //get search script based on query type eg. xquery, basic_search, advanced_search, autocomplete, autocomplete entry
            $python_search_file = $this->get_browse_path();
                
            //get matches from any type of search
            $permitted_params = escapeshellarg(json_encode($permitted));
            
            //$command = "python3 $python_search_file_arg $permitted_params";
            $command = "python3 $python_search_file $permitted_params";
            //extracts the json output object
            $raw_output = shell_exec($command);
            //echo $raw_output;
            //echo $raw_output["results"];
            $output = json_decode($raw_output, true);
            
            //store matches list
            $match_results = $output["results"];
            
            // add xml content to each entry in every page of the volume
            foreach ($match_results as &$page) {
                foreach ($page['records'] as &$record){
                    $entry_id = $record['id'];
                    $xml_path = $record['xmlpath'];
                    // add xml content to record
                    $record['xml_content'] = $this->get_xml_content($entry_id, $xml_path);
                    //echo $record['xml_content'];
                    // dont need to return the xmlpath so remove it
                    unset($record['xmlpath']);
                    }
            };

            $num_pages = (is_array($match_results) && count($match_results) > 0) ? count($match_results) : 0;

            //return results as an array;
            return [
                'success' => true,
                'num_pages' => $num_pages,
                'records' => $match_results,
                'message' => $output['message'] ?? '',
            ];
        } 
        catch (ValidationException $e){
            return null;
        }
        
    }

    public function get_browse_path(){
        return base_path('resources/python/browse_search.py');
        //return '../resources/python/browse_search.py';
    }
    

    /*
    XML file naming system:
    ARO-(beginning_volume)-(beginning_page)-(beginning_chapter)_ARO-(ending_volume)-(ending_page)-(ending_chapter).xml
    */
    public function get_xml_content($entry_id, $xml_path){
        $path = base_path($xml_path);
        // load the xml as a simple xml element
        $xml_file = simplexml_load_file($path);

        // Register the TEI namespace
        $xml_file->registerXPathNamespace('tei', $this->TEI_namespace);
        
        // get entry where xml:id is $id
        $target_xml = $xml_file->xpath("//tei:div[@xml:id='{$entry_id}']");

        // Check if the entry exists
        if (!empty($target_xml)) {
            return $target_xml[0]->asXML(); // Return the first match (or the only match)
        } else {
            return null; // Return null if no entry found
        }
    }
}
