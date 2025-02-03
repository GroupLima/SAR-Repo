<script setup>
import SearchResultCard from '@/components/SearchResultCard.vue';
import { reactive, onMounted } from 'vue';
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
    isLoading: true
});

const search = async() => {
    const baseSearchUrl = 'http://localhost:8000/api/search'
    console.log('im in search results');
    try {
        const response = await axios.get(baseSearchUrl, { params: props.queryParams,});
        console.log("results");
        console.log("data", response.data);
        if (response.data.success) {
            state.results = response.data.results;
            // Handle the response data (assuming it's structured like this)
            state.results = response.data.results || [];
            state.num_results = response.data.num_results;
            state.total_results = response.data.total_results || 0;
            state.frozen_variant = response.data.variant*10;
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
//search
</script>

<template>
    <div>
        <!-- Display the results dynamically -->
        <div class="results-section mt-3">
            <h2 class="results-title">Results</h2>
            <!-- <p v-if="numberOfXQuery">Number of Results: @{{ numberOfXQuery }}</p> -->
            <div v-if="!state.isLoading">
                <p>Showing {{ state.num_results }} / {{ state.total_results }} entries where the start of matches are limited to {{ state.frozen_variant }}% variance</p>
                <!-- show message if result exists -->
                <SearchResultCard class="result-item" v-for="(content, docId) in state.results" :key="docId" :id="docId" :htmlContent="content"/>
                <!-- <p>Debug: {{ state.results }}</p> -->
            </div>
            <div v-else>
                loading...
            </div>
                
        </div>

                 
    </div>
</template>