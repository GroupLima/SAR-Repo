@extends('layouts.app')
@section('title', 'XQuery Search')
@section('content')

<div class="container">

    <br><br><br><br><br><br><br><br><br><br><br><br><br><br>


    <header>
        <div class="header-content">
            <h1 id="xq-title">XQuery Search</h1>
            <p>Search through XML documents using XQuery</p>
        </div>
    </header>
    
    <main id="app">
        <div class="search-section">
            <div class="input">
            <input 
                type="search"
                placeholder="Enter your XQuery"
                v-model="query"
            />
            </div>
            <div class = "button">
            <button  @click="runQuery">Run Query</button>   
            </div>
        </div>
        
        <div v-if="error" class="alert alert-danger mt-3">
            @{{ error }}
        </div>
        
        <!-- Display the results dynamically -->    
        <div class="results-section mt-3">
            <h2 class="results-title">Results</h2>
            <p v-if="numberOfXQuery">Number of Results: @{{ numberOfXQuery }}</p>
            
            <div v-if="results" class="result-item" v-for="(content, id) in results" :key="id">
                 
                <h4>@{{ id }}</h4>
                
                <div v-html="content"></div> <!-- This will render the HTML content inside the div -->
                <br> 
            </div>
            
            <p>Debug: @{{ results }}</p>
        </div>

    </main>
</div>
@endsection

@section('scripts')
<script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const { createApp } = Vue;

    createApp({
        data() {
            return {
                query: '',
                results: null,
                error: null,
            };
        },
        methods: {
            async runQuery() {
                console.log("Run Query button clicked!");

                try {
                    // Reset previous results and error
                    this.results = null;
                    this.error = null;

                    // Send request with query data
                    const response = await axios.post('/xquery', {
                        query: this.query, // Sending the query entered by the user
                    });

                    console.log("Response received:", response);

                    // Check if the response contains data
                    if (response.data.message) {
                        const { numberOfXQuery, queryResults } = response.data.message;

                        // Handle the response data (assuming it's structured like this)
                        this.results = queryResults;
                        this.numberOfXQuery = numberOfXQuery
                        console.log("Number of results:", numberOfXQuery);
                    } else {
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
    }).mount('#app');
});

</script>

