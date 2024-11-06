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
@endsection