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
    <div class="app"> <!-- Mount Vue here using the class -->
        <div class="search-section">
            <div class="basic-search">
                <input
                    type="search"
                    placeholder="Enter your search term"
                    aria-label="Search"
                    id="search-box"
                    v-model="basicSearch"
                />
                <button id="search-button" @click="runQuery">SEARCH</button>
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


    <!-- Display the results dynamically -->
    <div class="results-section mt-3">
        <h2 class="results-title">Results</h2>
        <!-- <p v-if="numberOfXQuery">Number of Results: @{{ numberOfXQuery }}</p> -->
        <p v-if="total_results > 0">Showing @{{ num_results }} / @{{ total_results }} entries where the start of matches are limited to @{{ frozen_variant }}% variance</p>

        <div v-if="results" class="result-item" v-for="(content, id) in results" :key="id">
            <h4>@{{ id }}</h4>

            <div v-html="content"></div> <!-- This will render the HTML content inside the div -->
            <br>
        </div>
        <p>Debug: @{{ results }}</p>
    </div>

    <div class="image-container">
            <img src="{{ asset('images/sample.png') }}" alt="sample text" style="overflow: hidden;">
        </div>
    </div> <!-- End of Vue-controlled section -->
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

<!-- Load Vue and Axios after DOM is loaded -->
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const { createApp } = Vue;

    createApp({
        data() {
            return {
                isDropdownOpen: false,
                basicSearch: "per ka",
                methodSearch: "starts with",
                language: "any",
                variant: "1",
                volumes: "",
                pageSearch: "",
                entrySearch: "",
                startDate: "",
                endDate: "",
                docId: "",
                results: null,
                error: null,
            };
        },
        methods: {
            toggleDropdown() {
                this.isDropdownOpen = !this.isDropdownOpen;
            },
            async runQuery() {
                console.log("Run Query button clicked!");
                try {
                    this.results = null;
                    this.error = null;

                    const dataUser = {
                        basicSearch: this.basicSearch, //input
                        methodSearch: this.methodSearch, //keywords phrase etc
                        language: this.language,
                        variant: this.variant,
                        volumes: this.volumes,
                        pageSearch: this.pageSearch,
                        entrySearch: this.entrySearch,
                        startDate: this.startDate,
                        endDate: this.endDate,
                        docId: this.docId,
                    };
                    console.log('dataUser');
                    console.log(dataUser);
                    const response = await axios.get('/search', {
                        params: {
                            query_type: "basic_search", //basic , adnvaced etc...
                            basicSearch: this.basicSearch,
                            methodSearch: this.methodSearch,
                            language: this.language,
                            variant: this.variant,
                            volumes: this.volumes,
                            pageSearch: this.pageSearch,
                            entrySearch: this.entrySearch,
                            startDate: this.startDate,
                            endDate: this.endDate,
                            docId: this.docId,// Sending the query entered by the user
                        },

                    });
                    console.log("Response received:", response);
                    console.log("success?", response.data.success);
                    // Check if the response contains data
                    if (response.data.success) {
                        // const { numberOfXQuery, queryResults } = response.data.message;
                        const results = response.data.results;
                        console.log("debug results", results);
                        // Handle the response data (assuming it's structured like this)
                        this.results = results || [];
                        this.num_results = response.data.num_results;
                        this.total_results = response.data.total_results || 0;
                        this.frozen_variant = response.data.variant*10;
                        // this.numberOfXQuery = numberOfXQuery
                        // console.log("Number of results:", numberOfXQuery);
                    } else {
                        console.log("no debug results");
                        // Handle the case where the message is empty or malformed
                        this.error = "No results found!";
                    }

                } catch (error) {
                    console.error("Error occurred:", error.response.data);

                    // Check if the error response contains a message and handle it
                    if (error.response && error.response.data) {
                        this.error = error.response.data.error || 'An unexpected error occurred';
                    } else {
                        this.error = 'An unexpected error occurred';
                    }
                }
            }
        }
    }).mount('.app');  // Mount Vue on the div with class="app"
});
</script>
@endsection

