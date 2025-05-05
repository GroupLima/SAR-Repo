<?php

namespace App\Http\Controllers;

use Illuminate\Validation\ValidationException;
use Illuminate\Http\Request;


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
            //get search script based on query type eg. xquery, basic_search, advanced_search, autocomplete, autocomplete entry
            $python_search_file = $this->get_browse_path();
            
            //get matches from any type of search
            $permitted_params = escapeshellarg(json_encode($permitted));
            
            //$command = "python3 $python_search_file_arg $permitted_params";
            $command = "python3 $python_search_file $permitted_params";
            //extracts the json output object
            $raw_output = shell_exec($command);
            $output = json_decode($raw_output, true);
            
            //store matches list
            $match_results = $output["results"];

            // add xml content to each entry in every page of the volume
            foreach ($match_results as $page) {
                foreach ($page['records'] as &$record){
                    $entry_id = $record['id'];
                    $xml_path = $record['xmlpath'];

                    // add xml content to record
                    $record['xml_content'] = $this->get_xml_content($entry_id, $xml_path);
                    
                    // dont need to return the xmlpath so remove it
                    unset($record['xmlpath']);
                    }
            };

            // Check if $this->match_results is not null and is an array
            $num_pages = (is_array($match_results) && count($match_results) > 0) ? count($match_results) : 0;
            
            // Return the JSON response with the validated data
            return response()->json([
                'success' => true,
                'num_pages' => $num_pages,
                'records' => $match_results,
                'message' => $output['message'],
            ]);

        } catch (ValidationException $e){
            return response()->json([
                'success' => false,
                'message' => 'Invalid parameters for browse search',
                //route to valid error page eventually
            ]);
        }
    }

    public function get_browse_path(){
        return '../resources/python/browse_search.py';
    }
    
    public function get_xml_content($entry_id, $xml_path){
        // load the xml as a simple xml element
        $xml_file = simplexml_load_file($xml_path);

        // Register the TEI namespace
        $xml_file->registerXPathNamespace('tei', $this->TEI_namespace);
        
        // get entry where xml:id is $id
        $target_xml = $xml_file->xpath("//tei:div[@xml:id='{$entry_id}']");

        // Check if the entry exists
        if (!empty($target_xml)) {
            return $target_xml[0]; // Return the first match (or the only match)
        } else {
            return null; // Return null if no entry found
        }

        // 1. asXML converts simple xml into a string format
        // 2. htmlentities turns xml into a string and escapes special characters
        // 3. nl2br implements new lines as <br> html tag
        $converted_xml = nl2br(htmlentities($target_xml->asXML()));
        return $converted_xml;
    }

    // public function getVolumes()
    // {
    //     return response()->json([
    //         1 => 20,
    //         2 => 15,
    //         4 => 25,
    //         5 => 18,
    //         6 => 22,
    //         7 => 16,
    //         8 => 19,
    //     ]);
    // }

    // public function getRecords(Request $request)
    // {   
    //     $volume = $request->query('volume');

    //     if (!$volume) {
    //         return response()->json(['error' => 'Volume and page are required'], 400);
    //     }

    //     $directories = [
    //         storage_path('app/xml-files/XML files volumes 1-7'),
    //         storage_path('app/xml-files/XML files volume 8'),
    //     ];

    //     $records = [];

    //     // prepare to iterate through all entries of
    //     $entries = $this->jsonData[$volume] ?? [];



        
    //     foreach ($directories as $dir) {
    //         if (!is_dir($dir)) {
    //             \Log::error("Directory not found: $dir");
    //             continue;
    //         }

    //         foreach (scandir($dir) as $file) {
    //             if (!str_ends_with($file, '.xml')) continue;

    //             $filePath = $dir . DIRECTORY_SEPARATOR . $file;
    //             \Log::info("Processing file: $filePath");

    //             libxml_use_internal_errors(true);
    //             $xml = simplexml_load_file($filePath);

    //             if (!$xml) {
    //                 \Log::error("Failed to parse XML: " . print_r(libxml_get_errors(), true));
    //                 continue;
    //             }

    //             $xml->registerXPathNamespace('tei', 'http://www.tei-c.org/ns/1.0');
    //             $xml->registerXPathNamespace('xml', 'http://www.w3.org/XML/1998/namespace');

    //             $entries = $xml->xpath('//tei:div[@type="entry" or @type="incompleteEntry"]');

    //             foreach ($entries as $entry) {
    //                 $id = (string)$entry->attributes('xml', true)->id;
    //                 $lang = (string)$entry->attributes('xml', true)->lang;

    //                 // Filter for volume
    //                 if (!str_starts_with($id, 'ARO-' . $volume . '-')) {
    //                     continue;
    //                 }

    //                 // Get date from previous sibling
    //                 $date = '';
    //                 $precedingElements = $entry->xpath('preceding-sibling::tei:p[1]/tei:date[@when]');
    //                 if (!empty($precedingElements)) {
    //                     $date = (string)$precedingElements[0]['when'];
    //                 }

    //                 $content = '';
    //                 if ($entry->head) {
    //                     $content .= (string)$entry->head . "\n";
    //                 }
    //                 if ($entry->p) {
    //                     $content .= strip_tags($entry->p->asXML());
    //                 }

    //                 $records[] = [
    //                     'id' => $id,
    //                     'language' => $lang,
    //                     'content' => $content,
    //                     'date' => $date,
    //                 ];

    //                 \Log::info("Found entry: $id");
    //             }
    //         }
    //     }

    //     $perPage = 10;
    //     $offset = ($page - 1) * $perPage;
    //     $paginated = array_slice($records, $offset, $perPage);

    //     return response()->json([
    //         'records' => $paginated,
    //         'total' => count($records),
    //     ]);
    // }

    

    // public function getXml($id)
    // {
    //     $directories = [
    //         storage_path('app/xml-files/XML files volumes 1-7'),
    //         storage_path('app/xml-files/XML files volume 8'),
    //     ];

    //     foreach ($directories as $dir) {
    //         if (!is_dir($dir)) continue;

    //         foreach (scandir($dir) as $file) {
    //             if (!str_ends_with($file, '.xml')) continue;

    //             $filePath = $dir . DIRECTORY_SEPARATOR . $file;
    //             libxml_use_internal_errors(true);
    //             $xml = simplexml_load_file($filePath);
    //             if (!$xml) continue;

    //             $xml->registerXPathNamespace('tei', 'http://www.tei-c.org/ns/1.0');
    //             $xml->registerXPathNamespace('xml', 'http://www.w3.org/XML/1998/namespace');

    //             $entries = $xml->xpath('//tei:div[@xml:id="' . $id . '"]');
    //             if (!empty($entries)) {
    //                 $entry = $entries[0];
    //                 $dom = dom_import_simplexml($entry);
    //                 $xmlDoc = new \DOMDocument();
    //                 $xmlDoc->preserveWhiteSpace = false;
    //                 $xmlDoc->formatOutput = true;
    //                 $xmlDoc->appendChild($xmlDoc->importNode($dom, true));

    //                 libxml_clear_errors();
    //                 return response($xmlDoc->saveXML(), 200)
    //                     ->header('Content-Type', 'application/xml');
    //             }
    //         }
    //     }

    //     return response()->json(['error' => 'XML entry not found'], 404);
    // }
}
