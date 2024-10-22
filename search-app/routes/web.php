<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\RouteController;


//Default route for the home page
Route::get('/', [RouteController::class, 'display_view'])->defaults('page', 'home');

//route when user goes to a page
Route::get('/{page}', [RouteController::class, 'display_view']);