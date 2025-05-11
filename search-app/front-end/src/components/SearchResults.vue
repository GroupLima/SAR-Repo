<script setup>
import SearchResultCard from '@/components/SearchResultCard.vue';
import { reactive, onMounted, computed, ref, watch } from 'vue';
import axios from 'axios';
import '@/assets/sass/app.scss';
import router from '@/router';

const emit = defineEmits(['update:loading', 'update:message']);

const props = defineProps({
    queryParams: {
        type: Object,
        required: true
    },
    isLoading: {
        type: Boolean,
        default: false
    },
    userMessage: {
        type: String,
        default: ''
    }
});

const state = reactive({
    results: [],
    num_results: 0,
    total_results: 0,
    frozen_variant: 0,
    error: "",
    isLoading: false,
    current_page: 1,
    results_per_page: Number(props.queryParams.resultsPerPage) || 5,
    sort_by: props.queryParams.sortBy || 'Frequency in result',
    total_pages: 1,
    searchMethod: props.queryParams.methodSearch || 'word_start',
    variants: props.queryParams.variant || '0',
    displayResults: false
});

const goToPageNumber = ref(1);

// preferences
const searchMethods = [
    { value: 'keywords', text: 'Keywords' },
    { value: 'phrase', text: 'Phrase' },
    { value: 'regex', text: 'Regex' },
    { value: 'word_start', text: 'Word Start' },
    { value: 'word_middle', text: 'Word Middle' },
    { value: 'word_end', text: 'Word End' }
];
const varOptions = [0, 1, 2, 3, 4];
const rrpOptions = [5, 10, 20, 30, 50];
const ordOptions = ['Frequency within result', 'Best match', 'Volume, ascending', 'Volume, descending', 'Chronological'];

const filterChange = () => {
    state.current_page = 1;
    state.isLoading = true;
    router.push({ 
        query: { 
            ...props.queryParams, 
            methodSearch: state.searchMethod, 
            variant: state.variants 
        }
    });
    search();
}

const search = async() => {
    window.scrollTo({top: 0, behavior: 'smooth'});
    state.isLoading = true;
    state.error = '';
    emit('update:loading', true);
    emit('update:message', '');
    
    // Use a relative URL that will work on both localhost and production domain
    const baseSearchUrl = '/api/search';
    
    // Ensure query params include pagination information
    const searchParams = {
        ...props.queryParams,
        page: state.current_page,
        rpp: state.results_per_page,
        variant: state.variants,
        methodSearch: state.searchMethod,
        sort_by: state.sort_by,
    };
    
    try {
        // Add timeout to prevent long-hanging requests
        const response = await axios.get(baseSearchUrl, { 
            params: searchParams,
            timeout: 30000 // 30 seconds timeout
        });
        
        console.log("Search results:", response);
        
        if (response.data && (response.data.results || response.data.success)) {
            state.results = response.data.results || [];
            state.num_results = response.data.num_results || 0;
            state.total_results = response.data.total_results || 0;
            state.frozen_variant = response.data.variant * 10 || 0;
            state.total_pages = Math.ceil(state.total_results / state.results_per_page) || 1;
            state.displayResults = state.results.length > 0;
            
            if (state.results.length === 0) {
                emit('update:message', 'Sorry, no results found');
            }
        } else {
            console.log("No results or unexpected response format:", response);
            state.results = [];
            state.displayResults = false;
            emit('update:message', 'Sorry, no results found');
        }
    } catch (error) {
        state.results = []; // Ensure results are cleared on error
        state.displayResults = false;
        
        if (error.code === 'ECONNABORTED') {
            console.warn('Request timeout or cancelled:', error);
            emit('update:message', 'The search request timed out. Please try again with a more specific query.');
        } else if (axios.isCancel && axios.isCancel(error)) { 
            console.log('Search request was cancelled:', error.message);
            emit('update:message', 'Search request cancelled.');
        } else if (error.response && error.response.status === 500) {
            console.error('Backend server error (HTTP 500):', error);
            
            // If the error is about "Undefined array key page", provide a more specific message
            if (error.response.data && error.response.data.message && 
                error.response.data.message.includes('Undefined array key "page"')) {
                console.error('Page parameter missing:', error.response.data);
                // Retry the request with the page parameter explicitly added
                try {
                    const retryParams = {
                        ...searchParams,
                        page: 1  // Explicitly set page parameter
                    };
                    console.log('Retrying with explicit page parameter:', retryParams);
                    const retryResponse = await axios.get(baseSearchUrl, { 
                        params: retryParams,
                        timeout: 30000
                    });
                    if (retryResponse.data && retryResponse.data.results) {
                        state.results = retryResponse.data.results || [];
                        state.num_results = retryResponse.data.num_results || 0;
                        state.total_results = retryResponse.data.total_results || 0;
                        state.frozen_variant = retryResponse.data.variant * 10 || 0;
                        state.total_pages = Math.ceil(state.total_results / state.results_per_page) || 1;
                        
                        if (state.results.length === 0) {
                            emit('update:message', 'Sorry, no results found');
                        } else {
                            state.displayResults = true;
                        }
                    } else {
                        emit('update:message', 'Sorry, no results found');
                    }
                } catch (retryError) {
                    console.error('Retry also failed:', retryError);
                    emit('update:message', 'The search service is experiencing issues. Please try again later.');
                }
            } else {
                emit('update:message', 'The search service is currently experiencing issues. Please try again later or contact support if the problem persists.');
                
                // Log more specific error details for debugging if available
                if (error.response && error.response.data) {
                    console.error('Server error details:', error.response.data);
                }
            }
        } else {
            console.error('An unexpected error occurred while fetching search results:', error);
            emit('update:message', 'An error occurred while fetching search results. Please try again.');
        }
    } finally {
        state.isLoading = false;
        emit('update:loading', false);
    }
}

onMounted(search);
//search

// return an array of all page numbers
const pageNumbers = computed(() => {
    const numbers = [];
    for (let i = 1; i <= state.total_pages; i++) {
        numbers.push(i);
    }
    return numbers;
});
// returns the 4 numbers above and below the current page
const displayedPageNumbers = computed(() => {
    const startPage = Math.max(1, state.current_page-4);
    const endPage = Math.min(state.total_pages, state.current_page+4);
    return pageNumbers.value.slice(startPage-1, endPage,);
});

// SelectedPage
const selectedPage = (pageNumber) => {
    state.current_page = pageNumber;
    search();
}
// Next page
const nextPage = () => {
    if (state.current_page < state.total_pages) {
        state.current_page++;
        search();
    }
}
// Previous page
const prevPage = () => {
    if (state.current_page > 1) {
        state.current_page--;
        search();
    }
}
// first result of page
const firstResultOfPage = computed(() => 
    ((state.current_page - 1) * state.results_per_page) + 1
);
// last result of page
const lastResultOfPage = computed(() =>
    Math.min(state.current_page * state.results_per_page, state.total_results)
);

const goToSpecificPage = () => {
    if (goToPageNumber.value < 1) {
        goToPageNumber.value = 1;
        state.current_page = 1;
    } else if (goToPageNumber.value > state.total_pages) {
        goToPageNumber.value = state.total_pages;
        state.current_page = state.total_pages;
    } else {
        state.current_page = goToPageNumber.value;
    }
    search();
};

const handleKeyPress = (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
        goToSpecificPage();
    }
};

const handleInput = (event) => {
    event.target.value = event.target.value.replace(/\D/g, '');
};

const showHelpPage = () => {
    const routeUrl = router.resolve({ name: 'help' }).href;
    window.open(routeUrl, '_blank');
};

</script>

<template>
    <div class="search-page">

        <!-- Results -->
        <div class="results-section mt-3">
            <h2 class="results-title">Results page {{ state.current_page }}</h2>
            <!-- <p v-if="numberOfXQuery">Number of Results: @{{ numberOfXQuery }}</p> -->
            <div v-if="!state.isLoading">
                <p>Showing {{ firstResultOfPage }} to {{ lastResultOfPage }} of {{ state.total_results }} entries with {{ state.frozen_variant }}% variance</p>
                <!-- show message if result exists -->
                <SearchResultCard 
                    class="result-item" 
                    v-for="(result, docId) in state.results"
                    :key="docId"
                    :id="docId"
                    :htmlContent="result.highlighted_html"
                    :htmlvolume="result.volume" 
                    :htmlpage="result.page"
                    :date="result.date"
                    :htmllang="result.lang"
                />
                <!-- <p>Debug: {{ state.results }}</p> -->
            </div>
            <div v-else>
                Loading...
            </div>
        </div>

        <!-- Changing Pages -->
        <div v-if="state.total_pages > 1 & !state.isLoading" class="page-changer">
            <!-- previous button -->
            <button @click="prevPage" :disabled="state.current_page <= 1">
                Previous
            </button>
            <!-- numbered buttons -->
            <button class="page-number" v-for="activePage in displayedPageNumbers" :key="activePage"
                :class="{ active: activePage === state.current_page }" @click="selectedPage(activePage)"
                :disabled="activePage === state.current_page">
                {{ activePage }}
            </button>
            <!-- next button -->
            <button @click="nextPage" :disabled="state.current_page >= state.total_pages">
                Next
            </button>
        </div>

        <!-- Go to specific page -->
        <div class="go-to-page">
            <input type="number" v-model="goToPageNumber" min="1" :max="state.total_pages" @keypress="handleKeyPress" @input="handleInput" />
            <button @click="goToSpecificPage">Go to page</button>
        </div>

    </div>

</template>