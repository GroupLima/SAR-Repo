<!-- resources/views/home.blade.php -->

@extends('layouts.app')
@section('title', 'Home Page')
@section('content')
<!-- Header Section -->
<header>
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <div class="header-content">
        <div class="aro-description">Discover 8 Volumes</div>
    <p>Some text explaining search</p>
    <br><br>
    </div>
    <link rel="icon" type="image/x-icon" href="{{ asset('favicon.ico') }}">
</header>

<!-- Main Section -->
<main>
    <div class="search-section">
        <div class="basic-search">
            <input
                type="search"
                placeholder="Enter your search term"
                aria-label="Search"
                id="search-box"
            />
            <button id="search-button">SEARCH</button>
        </div>
        <div id="advanced" class="advanced-search-container">
            <button class="dropdown-button" @click="toggleDropdown">
                ADVANCED SEARCH ▼
            </button>
            <div v-if="isDropdownOpen" class="advanced-search-dropdown">
                <div id="search-options">
                    @include('home-views.search')
                </div>
            </div>
        </div>
        
        
    </div>
    <br><br>
    <div class="image-container">
        <img src="{{ asset('images/sample.png') }}" alt="sample text" style = "overflow: hidden;">
    </div>
    @include('layouts.entries')
    <!-- this script isn't actually doing anyhing because it is linked to a class, not an id, so it
        doesn't work. Removing it has no effect because the vue script linked at the bottom is fully in
        control of the dropdown functionality. I don't think we need this.-->
    <!-- <script>
        function toggleDropdown() {
        document.getElementById("advanced-search-dropdown").classList.toggle("active");
        }
    </script> -->
    
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

</body>

@endsection
