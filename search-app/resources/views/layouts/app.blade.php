<!-- resources/views/layouts/app.blade.php -->

<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title')</title> <!-- Default title, can be overridden -->
</head>
<body>
    @yield('style', 'resources.css.app')
    @include('layouts.basic-navbar')   <!-- insert php content from other views -->
    @yield('content') <!-- Section for different page content -->
</body>
</html>
