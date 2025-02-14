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

    // The paths that will be accessible via CORS. Adjust if necessary.
    'paths' => ['api/*'],

    // Allow all HTTP methods (GET, POST, etc.)
    'allowed_methods' => ['*'],

    // Specify the origins allowed to access your API.
    // For development, allow only the Vite dev server URL.
    'allowed_origins' => ['http://localhost:5173', 'http://localhost:8000'],

    // If you need to use regex patterns for origins, you can use this.
    'allowed_origins_patterns' => [],

    // Allow all headers in requests.
    'allowed_headers' => ['*'],

    // Headers that should be exposed to the browser.
    'exposed_headers' => [],

    // Indicates how long (in seconds) the results of a preflight request can be cached.
    'max_age' => 0,

    // Whether the response to the request can be exposed when credentials are present.
    'supports_credentials' => false,
];