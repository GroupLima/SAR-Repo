<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class RouteController extends Controller
{
    //take in a string variable $page and returns the route if it exists
    public function display_view($page='/'){
        if (view()->exists($page)){
            return view('/' . $page);
        }
        //if the route doesn't exists, return a 404 error or a custom error page
        abort(404);
    }
    
}
