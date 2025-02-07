<?php
return [

     /*
    |--------------------------------------------------------------------------
    | Cross-Origin Resource Sharing (CORS) Configuration
    |--------------------------------------------------------------------------
    |
    | Here you may configure your settings for cross-origin resource sharing
    | or "CORS". This determines what cross-origin operations may execute
    | in web browsers. You are free to adjust these settings as needed.
    |
    */

    //'paths' => ['api/*', 'sanctum/csrf-cookie'],
    'paths' => ['api/*'],
    'allowed_methods' => ['*'],
    'allowed_origins' => [
        /*put development and production app url here */
        'http://localhost:5173','http://localhost:8000'
    ],
    'allowed_origins_patterns' => [],
    'allowed_headers' => ['*'],
    'exposed_headers' => [],
    'max_age' => 0,
    'supports_credentials' => false,
];