

<template>
    <div class="search-section">
        <basic-search-section @update-query="updateQuery"></basic-search-section>

        <div id="advanced" class="advanced-search-container">
            <button class="dropdown-button" @click="toggleDropdown">
                ADVANCED SEARCH ▼
            </button>
            <div v-if="isDropdownOpen" class="advanced-search-dropdown">
                <div id="search-options">
                    <advanced-search-section
                        @update-search-method="UpdateSearchMethod"
                        @update-variance="UpdateVariance"
                        >
                    </advanced-search-section>
                    <!--@include('home-views.search')-->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        data() {
            return {
                
                isDropdownOpen: false,
                results: null,
                error: null,
                params: {
                    qt : 'basic_search',
                    query : '',
                    rpp : 10,
                    'var' : 1,
                    ob : '',
                    sm : 'starts with',
                    entry_id : '',
                    date_from : '',
                    date_to : '',
                    vol : '',
                    pg : '',
                    pr : '',
                    page : ''
                },
            };
        },
        methods: {
            updateQuery(query){ this.params.query = query; },
            updateVariance(variance) { this.params.var = variance; },
            UpdateSearchMethod(search_method) { this.params.sm = search_method},

            async handleSearch(params) {
                try {
                    // Example: Make an API call using the `params` from the child component.
                    const response = await fetch('/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(params),
                    });
                    if (!response.ok) {
                        throw new Error('Search request failed');
                    }
                    const data = await response.json();
                    this.results = data.results;
                    this.error = null; // Clear any previous error
                } catch (err) {
                    this.error = err.message;
                    this.results = null; // Clear results if there's an error
                }
            },
        },
    }
</script>

<style scoped>
/* Add your styles for this component here */
</style>