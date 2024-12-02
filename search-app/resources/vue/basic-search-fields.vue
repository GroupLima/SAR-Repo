<!-- ./resources/vue/basic-search-fields.vue -->

<template>
    <div class="search-section">
        <div class="basic-search">
            <input
                type="search"
                v-model="params.query"
                placeholder="Enter your search term"
                @change="updateQuery(placeholder)"
                aria-label="Search"
                id="search-box"
            />
            <button @click="search" id="search-button">SEARCH</button>
        </div>
        </div>
</template>

<script>
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
        methods: {
            
            updateQuery(query) { this.$emit('update-query', query); },
            search() { this.$emit('runSearch', this.params); },
        }
    }
</script>

<style scoped>
/* Add your styles for this component here */
</style>