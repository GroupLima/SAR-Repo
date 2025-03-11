<script setup>
import SearchResultCard from '@/components/SearchResultCard.vue';
import { reactive, onMounted, computed } from 'vue';
import axios from 'axios';

const props = defineProps({
    queryParams: {
        type: Object,
        required: true
    }
});

const state = reactive({
    results: [],
    num_results: 0,
    total_results: 0, //dummy data
    frozen_variant: 0,
    error: "",
    isLoading: true,
    current_page: 1,
    results_per_page: 5,
    total_pages: 1,
    searchMethod: props.queryParams.sm || 'word_start',
    variants: props.queryParams.var || '0'
});

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
const ordOptions = ['Frequency within result', 'Volume, ascending', 'Volume, descending', 'Chronological'];

function filterChange() {
    state.current_page = 1;
    state.isLoading = true;
    search();
}

const search = async() => {
    window.scrollTo({top: 0, behavior: 'smooth'});
    const baseSearchUrl = 'http://localhost:8000/api/search'
    //console.log('im in search results');
    const searchParams = {
        ...props.queryParams,
        page: state.current_page,
        rpp: state.results_per_page,
        var: state.variants,
        sm: state.searchMethod
    };
    try {
        const response = await axios.get(baseSearchUrl, { params: searchParams,});
        //console.log("results");
        //console.log("data", response.data);
        if (response.data.success) {
            state.results = response.data.results;
            // Handle the response data (assuming it's structured like this)
            state.results = response.data.results || [];
            state.num_results = response.data.num_results;
            state.total_results = response.data.total_results || 0;
            state.frozen_variant = response.data.variant*10;
            state.total_pages = Math.ceil(state.total_results / state.results_per_page);
        } else {
            console.log("no debug results");
            console.log(response);
            // Handle the case where the message is empty or malformed
            //state.error = "No results found!";
        }
    } catch (error) {
        console.error("error fetching results", error);
    } finally {
        //console.log("setting load value to false");
        state.isLoading = false;
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
function selectedPage(pageNumber) {
    state.current_page = pageNumber;
    search();
}
// Next page
function nextPage() {
    if (state.current_page < state.total_pages) {
        state.current_page++;
        search();
    }
}
// Previous page
function prevPage() {
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

</script>

<template>
    <div class="search-page">

        <!-- Preferences -->
        <div class="preferences">
            <div class="preference-item">
                <label>Search method:</label>
                <select id="searchMethod" v-model="state.searchMethod" @change="filterChange">
                    <option v-for="sm in searchMethods" :key="sm.value" :value="sm.value">{{ sm.text }}</option>
                </select>
            </div>
            <div class="preference-item">
                <label>Variants:</label>
                <select id="variants" v-model="state.variants" @change="filterChange">
                    <option v-for="variants in varOptions" :key="variants" :value="variants">{{ variants }}</option>
                </select>
            </div>
            <div class="preference-item">
                <label>Results per page:</label>
                <select id="resultsPerPage" v-model="state.results_per_page" @change="filterChange">
                    <option v-for="rpp in rrpOptions" :key="rpp" :value="rpp">{{ rpp }}</option>
                </select>
            </div>
            <div class="preference-item">
                <label>Sort by:</label>
                <select>
                    <option v-for="ord in ordOptions">{{ ord }}</option>
                </select>
            </div>
        </div>

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
                    :htmldate="result.date"
                />
                <!-- <p>Debug: {{ state.results }}</p> -->
            </div>
            <div v-else>
                loading...
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

    </div>
</template>