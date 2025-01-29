<!-- resources/views/about.blade.php -->

@extends('layouts.app')
@section('title', 'About Page')
@section('content')
<header>
    <div class="header-content">
        <h2>This is the about page</h2>
    </div>
</header>

<main>
    <div class="about-section">
        <div class="about-rows">
            <div class="about-column">one</div>
            <div class="about-column">two</div>
            <div class="about-column">three</div>
        </div>
    </div>
</main>

<footer>
    <div class="footer-links">
        <a href="#">IMPORTANT LINKS</a>
        <a href="#">BLOG PAGE</a>
        <a href="#">UNIVERSITY ARO PAGE</a>
        <a href="#">ACKNOWLEDGMENTS</a>
    </div>
</footer>
<script>
    // Function to transition to a new page with fade out effect
    window.transitionToPage = function(href) {
        // Fade out the body
        document.querySelector('body').style.opacity = 0;

        // After 500ms (duration of the fade-out), navigate to the new page
        setTimeout(function() { 
            window.location.href = href;
        }, 500); // This timeout should match the fade-out duration
    }

    // When the page is fully loaded, fade it in
    window.addEventListener("load", (event) => {
        // Fade in the body
        document.querySelector('body').style.opacity = 1;
    });
</script>
@endsection