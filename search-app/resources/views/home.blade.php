@extends('layouts.app')
@section('title', 'Home Page')
@section('content')
<!-- Header Section -->
<header>
    <div class="header-content">
        <div class="aro-description">ARO DESCRIPTION</div>
    </div>
    <link rel="icon" type="image/x-icon" href="{{ asset('favicon.ico') }}">
</header>

<!-- Main Section -->
<main>
    <div class="search-section">
        <div class="basic-search">
            <input
                type="search"
                placeholder="Enter your search term"s
                aria-label="Search"
            />
            <button @click="dataStored">SEARCH</button> <!-- Fixed @dataStored to @click="dataStored" -->
        </div>
        <div id="advanced" class="advanced-search-container">
            <button class="dropdown-button" @click="toggleDropdown">
                ADVANCED SEARCH ▼
            </button>
            <div v-if="isDropdownOpen" class="advanced-search-dropdown">
                <div id="search-options">
                    @include('home-views.search')
                    <!-- sass people please make this section wider, i.e. not just the width of the button -->
                    <!-- it truly looks so sad and squished rn, so the empty space needs utilised -->
                    <!-- also shouldnt cover content when it pops up -->
                </div>
            </div>
        </div>
        @include('layouts.entries')
    </div>
</main>

<!-- Footer Section -->
<footer>
    <div class="footer-links">
        <a href="#">IMPORTANT LINKS</a>
        <a href="#">BLOG PAGE</a>
        <a href="#">UNIVERSITY ARO PAGE</a>
        <a href="#">ACKNOWLEDGMENTS</a>
    </div>
</footer>

<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<script src="{{ asset('compiled-js/home.js') }}"></script>
@endsection
