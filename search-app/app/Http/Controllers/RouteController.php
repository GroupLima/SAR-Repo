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
    public function display_view($page='/'){
        if ($this->valid_route($page)){
            if ($page == 'home'){
                $this->xmlController->display_entries();
                return view('home', compact('entries'));
            }
            return view('/' . $page);
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
    
}
