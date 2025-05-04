<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\RouteController;
use App\Http\Controllers\SearchController;
use App\Http\Controllers\TestController;
use App\Http\Controllers\RecordController;
use Illuminate\Support\Facades\File;


/*
put all application routes here with their corresponding functions
*/

// API Routes (serve as backend)
Route::prefix('/api')->group(function () {
    Route::get('/test-request', [TestController::class, 'test']);
    Route::get('/search', [SearchController::class, 'search']);
    Route::get('/xquery', [SearchController::class, 'runXQuery']);

    Route::get('/volumes', [RecordController::class, 'getVolumes']);
    Route::get('/records', [RecordController::class, 'getRecords']);
    Route::get('/records/{id}/xml', [RecordController::class, 'getXml']);
    
});

Route::get('/{any}', function () {
    return File::get(public_path('index.html'));
})->where('any', '.*');