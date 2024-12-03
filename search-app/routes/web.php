<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\RouteController;
use App\Http\Controllers\SearchController;


/*
put all application routes here with their corresponding functions
*/

//Default route for the home page
Route::get('/', [RouteController::class, 'display_view'])->defaults('page', 'home');
Route::get('/home', [RouteController::class, 'display_view'])->defaults('page', 'home');

//execute search function
Route::get('/search', [SearchController::class, 'search']);

//execute xquery
Route::post('/xquery', [SearchController::class, 'runXQuery']);

//execute run basic
Route::get('/runBasic', [SearchController::class, 'runBasic']);

//(always put on bottom so it doesn't override other routes)
//Route::get('/{page}', [RouteController::class, 'display_view']);

