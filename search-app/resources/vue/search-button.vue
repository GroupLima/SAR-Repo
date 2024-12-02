<template>
    <div class="search-section">
        <basic-search-section></basic-search-section>
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
            }          
        }
    }
</script>

<style scoped>
/* Add your styles for this component here */
</style>