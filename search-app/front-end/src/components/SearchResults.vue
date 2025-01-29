<script setup>
import SearchResultCard from '@/components/SearchResultCard.vue';
import { reactive } from 'vue';
import cursiveLatin from '@/assets/images/sample.png'
import axios from 'axios';

const props = defineProps({
    queryParams: [],
    
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
        const request = "" // construct request using queryParams
        const response = await axios.get(request); // insert route to back end to get 
        if (response.data.success) {
            // const { numberOfXQuery, queryResults } = response.data.message;
            state.results = response.data.results;
            console.log("debug results", results);
            // Handle the response data (assuming it's structured like this)
            state.results = results || [];
            state.num_results = response.data.num_results;
            state.total_results = response.data.total_results || 0;
            //this.frozen_variant = response.data.variant*10;
        } else {
            console.log("no debug results");
            // Handle the case where the message is empty or malformed
            state.error = "No results found!";
        }
    } catch (error) {
        console.error("error fetching results", error);
    } finally {
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

        <div class="image-container">
            <img :src="cursiveLatin" alt="sample text" style="overflow: hidden;">
        </div>           
    </div>
</template>