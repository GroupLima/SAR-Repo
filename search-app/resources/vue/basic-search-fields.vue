<!-- ./resources/vue/basic-search-fields.vue -->

<template>
    <div class="search-section">
        <div class="basic-search">
            <input
                type="search"
                v-model="params.query"
                placeholder="Enter your search term"
                aria-label="Search"
                id="search-box"
            />
            <button id="search-button">SEARCH</button>
        </div>
        </div>
</template>

<script>
    import axios from 'axios';
    export default {
        data() {
            return {
                params: {
                    qt : 'basic_search',
                    query : '',
                    'var' : 1,
                    rpp : 10,
                    sm : 'starts with',

                },
                results: null,
                error: null,
            };
        },
    }
</script>

<style scoped>
/* Add your styles for this component here */
</style>