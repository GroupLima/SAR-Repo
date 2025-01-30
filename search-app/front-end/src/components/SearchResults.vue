<script setup>
import SearchResultCard from '@/components/SearchResultCard.vue';
import { reactive, onMounted } from 'vue';
import axios from 'axios';

const props = defineProps({
    queryParams: Object
    
});

const state = reactive({
    results: [],
    num_results: 0,
    total_results: 0, //dummy data
    error: "",
    isLoading: true
});

const search = async() => {
    try {
        
        const response = await axios.get('/sar-db/search', {
            params: {
                query_type: "basic_search", //basic , adnvaced etc...
                basicSearch: state.results.basicSearch,
                methodSearch: state.results.methodSearch,
                language: state.results.language,
                variant: state.results.variant,
                volumes: state.results.volumes,
                pageSearch: state.results.pageSearch,
                entrySearch: state.results.entrySearch,
                startDate: state.results.startDate,
                endDate: state.results.endDate,
                docId: state.results.docId,// Sending the query entered by the user
            },
        
        }); 
        console.log("results");
        console.log(response.data);
        if (response.data.success) {
            // const { numberOfXQuery, queryResults } = response.data.message;
            state.results = response.data.results;
            console.log("debug results", results);
            // Handle the response data (assuming it's structured like this)
            state.results = results || [];
            state.num_results = response.data.num_results;
            state.total_results = response.data.total_results || 0;
            //state.results.frozen_variant = response.data.variant*10;
        } else {
            console.log("no debug results");
            console.log(response);
            // Handle the case where the message is empty or malformed
            //state.error = "No results found!";
        }
    } catch (error) {
        console.error("error fetching results", error);
    } finally {
        console.log("setting load value to false");
        state.isLoading = false;
    }
}

onMounted(search);
</script>

<template>
    <div>
        <!-- Display the results dynamically -->
        <div class="results-section mt-3">
            <h2 class="results-title">Results</h2>
            <!-- <p v-if="numberOfXQuery">Number of Results: @{{ numberOfXQuery }}</p> -->
            <div v-if="!state.isLoading">
                <p>Showing {{ num_results }} / {{ total_results }} entries where the start of matches are limited to @{{ frozen_variant }}% variance</p>
                <!-- show message if result exists -->
                <SearchResultCard class="result-item" v-for="(content, id) in results" :key="id" />
                <p>Debug: @{{ results }}</p>
            </div>
            <div v-else>
                loading...
            </div>
                
        </div>

                 
    </div>
</template>