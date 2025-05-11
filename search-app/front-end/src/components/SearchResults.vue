<script setup>
import SearchResultCard from '@/components/SearchResultCard.vue';
import { reactive, onMounted, computed, ref } from 'vue';
import axios from 'axios';
import '@/assets/sass/app.scss';
import router from '@/router';

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
    results_per_page: Number(props.queryParams.resultsPerPage) || 5,
    sort_by: props.queryParams.sortBy || 'Frequency in result',
    total_pages: 1,
    searchMethod: props.queryParams.methodSearch || 'word_start',
    variants: props.queryParams.variant || '0'
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
    // Use a relative URL that will work on both localhost and production domain
    const baseSearchUrl = '/api/search'
    //console.log('im in search results');
    const searchParams = {
        ...props.queryParams,
        page: state.current_page,
        rpp: state.results_per_page,
        variant: state.variants,
        methodSearch: state.searchMethod,
        sort_by: state.sortBy,
    };
    try {
        const response = await axios.get(baseSearchUrl, { params: searchParams,});
        console.log("results", response);
        //console.log("data", response.data);
        if (response.data.success) {
            state.results = response.data.results;
            // Handle the response data (assuming it's structured like this)
            state.results = response.data.results || [];
            state.num_results = response.data.num_results;
            state.total_results = response.data.total_results || 0;
            state.frozen_variant = response.data.variant*10;
            state.total_pages = Math.ceil(state.total_results / state.results_per_page);
            //console.log('date', state.results['ARO-5-0333-01'].date);
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
            <!-- <p v-if="numberOfXQuery">Number of Results: @{{ numberOfXQuery }}</p> -->
            <div v-if="!state.isLoading">
                <div v-if="state.total_results>0">
                    <h2 class="results-title">Results page {{ state.current_page }}</h2>
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
                </div>
                <div v-else>
                    <h2 class="results-title">No results found</h2>
                    <p>
                        Your search
                        <span v-if="props.queryParams.basicSearch != '*'"> - {{ props.queryParams.basicSearch }} - </span>
                        did not match any documents
                    </p>
                </div>
            </div>
            <div v-else>
                loading...
            </div>
        </div>

        <!-- Changing Pages -->
        <div v-if="state.total_results > 0 & !state.isLoading">
            <div class="page-changer">
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
    </div>

</template>