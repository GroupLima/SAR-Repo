<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\RouteController;
use App\Http\Controllers\SearchController;


//Default route for the home page
Route::get('/', [RouteController::class, 'display_view'])->defaults('page', 'home');

//route when user goes to a page
Route::get('/{page}', [RouteController::class, 'display_view']);

//execute search function
Route::get('/search', [SearchController::class, 'search']);

//execute xquery
Route::get('/xquery', [SearchController::class, 'xquery']);