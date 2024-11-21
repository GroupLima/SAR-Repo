<!-- resources/views/layouts/app.blade.php -->

<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title')</title> <!-- Default title, can be overridden -->
    <link rel="stylesheet" type="text/css" href="{{ asset('css/app.css') }}">
</head>
<body>
    @include('layouts.basic-navbar')   <!-- insert php content from other views -->
    <div id="content-wrapper">
    @yield('content') <!-- Section for different page content -->
    </div>
</body>
</html>


<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
    $(document).ready(function () {
        // Fade in content when the page loads
        $('#content-wrapper').fadeIn(1100); // 1.1 seconds fade-in

        // Handle navigation dynamically
        $('.nav-links a').on('click', function (e) {
            e.preventDefault(); // Prevent default page reload
            const url = $(this).attr('href'); // Get the target URL

            // Fade out the main content
            $('#content-wrapper').fadeOut(1000, function () {
                // After fade-out, load new content dynamically
                $.get(url, function (data) {
                    // Ensure you're receiving the correct content
                    console.log(data); // Log the response for debugging
                    console.log("Navigating to URL:", url);
                    // Extract the new content from the response (the entire page content)
                    const newContent = $(data).find('#content-wrapper').html(); 
                    console.log("newContent:", newContent);
                    $('#content-wrapper').html(newContent).fadeIn(1000); // Replace and fade-in the new content
                }).fail(function () {
                    alert('Failed to load content.');
                    $('#content-wrapper').fadeIn(1000); // Recover if AJAX fails
                });
            });
        });
    });
</script>
