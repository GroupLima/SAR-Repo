<script setup>
import SearchFields from '@/components/SearchFields.vue';
import SearchResults from '@/components/SearchResults.vue';
import { reactive, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const state = reactive({
    displayResults: false,
    queryParams: {}, // Initialize as object
    isLoading: false,
    userMessage: ''
});

const route = useRoute();
const router = useRouter();

const isValidQuery = (params) => {
    // Basic validation: ensure at least one query parameter has a non-empty value
    if (!params || typeof params !== 'object' || Object.keys(params).length === 0) {
        return false;
    }
    // Check if any value in the params object is non-empty and not null
    return Object.values(params).some(value => value !== null && String(value).trim() !== '');
};

// Watch for changes in route query parameters
watch(() => route.query, (newQueryParams) => {
    // Deep compare current state.queryParams with newQueryParams from route
    // This is to avoid re-fetching if the query object reference changes but values are the same,
    // or if router.push was called with the exact same query.
    const newQueryString = JSON.stringify(newQueryParams);
    const currentQueryString = JSON.stringify(state.queryParams);

    if (newQueryString !== currentQueryString) {
        if (isValidQuery(newQueryParams)) {
            console.log("Route query changed, updating params:", newQueryParams);
            // Make sure to include the page parameter to prevent backend errors
            const paramsWithPage = { 
                ...newQueryParams,
                page: newQueryParams.page || 1 // Always ensure page parameter exists
            };
            state.queryParams = { ...paramsWithPage }; // Update internal state
            state.displayResults = true; // Show the SearchResults component
            state.userMessage = ''; // Clear previous messages
        } else {
            // Query params were removed or became invalid (e.g., all empty)
            console.log("Route query cleared or invalid:", newQueryParams);
            state.displayResults = false;
            state.queryParams = { ...newQueryParams }; // Reflect the cleared/invalid query state
            state.userMessage = ''; // Clear any messages, or set a default like "Enter search criteria"
        }
    }
}, { deep: true, immediate: true }); // `immediate: true` runs the watcher on component initialization

// This function will be called when SearchFields emits an event (e.g., 'search-initiated')
const handleSearchInitiated = (searchParamsFromFields) => {
    if (isValidQuery(searchParamsFromFields)) {
        // Ensure page parameter is included to prevent backend errors
        const paramsWithPage = {
            ...searchParamsFromFields,
            page: searchParamsFromFields.page || 1
        };
        // Update the URL. The watcher will pick up this change and trigger fetchSearchResults.
        router.push({ query: paramsWithPage });
    } else {
        // If search params are invalid (e.g., all fields cleared by user in SearchFields)
        // Clear the query in the URL, which the watcher will also pick up.
        router.push({ query: {} });
        // User message for invalid/empty search can be set here or handled by the watcher
        // state.userMessage = 'Please enter search criteria.';
        // state.displayResults = false;
        // state.searchResults = [];
    }
};

</script>

<template>
    <div class="search-page">
        <!-- Main Section -->
        <main class="content">
            <SearchFields @search-initiated="handleSearchInitiated" />
            <!-- <div v-if="state.isLoading" class="loading-spinner-container">
                <div class="loading-spinner"></div>
            </div> -->
            <div v-if="state.userMessage && !state.isLoading" class="user-message" role="alert">
                {{ state.userMessage }}
                <!-- Add additional guidance for server errors -->
                <div v-if="state.userMessage.includes('service is currently experiencing issues')" class="error-guidance">
                    <p>This might be due to:</p>
                    <ul>
                        <li>The search service being temporarily down</li>
                        <li>A complex query that requires more processing time</li>
                        <li>Connection issues between the frontend and backend services</li>
                    </ul>
                    <p>You can try:</p>
                    <ul>
                        <li>Simplifying your search terms</li>
                        <li>Refreshing the page and trying again</li>
                        <li>Coming back in a few minutes</li>
                    </ul>
                </div>
            </div>
            <div v-if="state.displayResults && !state.userMessage">
                <SearchResults 
                    :queryParams="state.queryParams" 
                    @update:loading="(value) => state.isLoading = value"
                    @update:message="(value) => state.userMessage = value"
                /> 
            </div>
        </main>
    </div>
</template>

<style scoped>
/* .loading-spinner-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border-left-color: #09f;
    margin-bottom: 10px;

    animation: spin 1s ease infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
} */

.user-message {
    text-align: center;
    padding: 15px;
    margin-top: 15px;
    border-radius: 4px;
    background-color: #f8f9fa;
    border-left: 4px solid #6e0d25;
}

.error-guidance {
    text-align: left;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid rgba(0,0,0,0.1);
}

.error-guidance p {
    margin-bottom: 8px;
    font-weight: 500;
}

.error-guidance ul {
    margin-bottom: 15px;
    padding-left: 20px;
}

.error-guidance li {
    margin-bottom: 5px;
    font-size: 0.95em;
}

body.dark .user-message {
    background-color: #2a2a2a;
    border-left: 4px solid #6e0d25;
    color: white;
}

body.dark .error-guidance {
    border-top: 1px solid rgba(255,255,255,0.1);
}
</style>
