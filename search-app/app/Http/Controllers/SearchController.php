<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class SearchController extends Controller
{
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

    function simplify_search_params($params){
        //params: user query, results per page, variance, order by asce/desc, search method, entry id, date from, date to, volume, page, paragraph, language, page number
        $param_keys = ['query', 'rpp', 'var', 'ob', 'sm', 'entry_id', 'date_from', 'date_to', 'vol', 'pg', 'pr', 'lang', 'page'];
        $ermitted = [];
        foreach ($param_keys as $param){
            if (isset($params[$param])) {
                $permitted[$param] = $params[$param];
            }
        }
        return $permitted;
    }

    
    function search(Request $request){
        // extracts params from request
        // deals with both basic and advanced search
        // params is a dictionary of key value pairs
        // params: user query, results per page, variance, order by asce/desc, search method, entry id, date from, date to, volume, page, paragraph, language, page number
        $params = $request->query(); // insert params from request here
        $permitted = $this->simplify_search_params($params);
        $python_search_file = './search-app/resources/python/Search.py ' . $permitted;
        $matches = shell_exec('python3 ' . $python_search_file);
        return $matches;
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
    // autocomplete for user query
    function autocomplete(){
        // uses search
        // min length to apply autocomplete: 2
    }

    // autocomplete for entry ID
    function autocomplete_entry(){
        // uses search
        // min length to apply autocomplete: 2
    }


    function chart_wordstart_date(){
        // uses search
    }
}
