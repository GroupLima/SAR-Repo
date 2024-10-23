<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class XmlController extends Controller
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
    2. returns results found:
        a. number of matches per entry
        b. index, length, and spelling variant of each match in each result


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

    //handles user request which is a dictionary of filters
    function assign_filters(Request $search_args){
        /*ex.  $search_args = [ 
                        "language" => "latin",
                        "page" => "5, 18, 9",
                        "paragraph" = None, 
                        etc...
                    ];
        $search_args["language"]; will return "latin"
        */

    }




}
