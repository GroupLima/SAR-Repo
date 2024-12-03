<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class RouteController extends Controller
{
    protected $xmlController;

    public function __construct(XmlController $xmlController)
    {
        $this->xmlController = $xmlController;
    }

    //take in a string variable $page and returns the route if it exists
    // added check so that xml isn't displayed on home page for no reason :)
    public function display_view($page='/', $displayEasterEgg = false){
        if ($this->valid_route($page)){
            if ($page == 'home'){
                $entries = [];
                if ($displayEasterEgg == true){
                    $entries = $this->xmlController->get_all_entries();
                }
                return $this->xmlController->display_entries($entries);
            }
            return view($page); //changed
        }
        //if the route doesn't exists, return a 404 error or a custom error page
        abort(404);
    }

    public function valid_route($page){

        if (view()->exists($page)){
            return true;
        }
        // add other validations if needed
        // ...

        // if did not pass any of the validation checks, return false
        return false;
    }
    // Route for search (added this method to integrate SearchController)
    /*
    public function search(Request $request)
    {
        $searchController = new SearchController();
        return $searchController->search($request);
    }*/
}


