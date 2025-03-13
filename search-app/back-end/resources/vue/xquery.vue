<!-- ./resources/vue/xquery.vue -->

<template>
    <div class="search-section">
        <input 
            type="search"
            placeholder="Enter your XQuery"
            v-model="query"
            id="xq-box"
            class="form-control"
        />
            <button id="xq-button" @click="runQuery" class="btn btn-primary">Run Query</button>   
        </div>
        
        <div v-if="error" class="alert alert-danger mt-3">
            @{{ error }}
        </div>
        
        <div class="results-section mt-3">
            <h2 class="results-title">Results</h2>
            <pre v-if="results" id="xq-results" class="xml-results">@{{ results }}</pre>
            <p>Debug: @{{ results }}</p>
        </div>
</template>

<script>
    import axios from 'axios';
    export default {
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
                    this.results = null;
                    this.error = null;

                    const response = await axios.post('/xquery', {
                        query: this.query,
                    });

                    console.log("Response received:", response);
                    this.results = response.data.message;
                } catch (error) {
                    console.error("Error occurred:", error);
                    this.error = error.response?.data?.error || 'An unexpected error occurred';
                }
            }          
        }
    }
</script>
