<script setup>
import { reactive, onMounted } from 'vue';
import axios from 'axios';
import Footer from '@/components/Footer.vue';

const props = defineProps({
    queryParams: {
        type: Object,
        required: true
    }
});
const state = reactive({
    query: '',
    results: [],
    num_results: 0,
    total_results: 0,
    error: "",
    isLoading: false,
    start: 1,    // Default start index
    count: 10,    // Default count per page
});

const runQuery = async () => {
    const XQeuryURL = 'http://localhost:8000/api/xquery'
    console.log("Run Query button clicked!");
    state.isLoading = true;
    state.results = [];
    state.error = "";

    try {
        const response = await axios.get(XQeuryURL, {
            params: {
                query_type: "xquery",
                query: state.query,
                exist_start: state.start,  // Pass start value
                exist_count: state.count   // Pass count value
            },
        });
        console.log("Response received:", response);
        if (response.data.message) {
            // Directly map response to state.results
            const xmlString = response.data.message.queryResults;
            console.log(typeof xmlString, xmlString);
            const xmlPretty = window.vkbeautify.xml(xmlString, 5);
            state.results = xmlPretty;
            console.log("happy",state.results);
        } else {
            state.error = "No results found!";
        }
    } catch (error) {
        console.error("Error occurred:", error);
        state.error = error.response?.data?.error || 'An unexpected error occurred';
    } finally {
        state.isLoading = false;
    }
};
</script>

<template>
    <div class="xquery-page">
        <header>
            <div class="header-content">
                <br><br><br><br>
                <h1>XQuery Search</h1>
                <p>Search through XML documents using XQuery</p>
            </div>
        </header>
        
        
        <main>
            <div class="search-section">
                <div class="basic-search">
                    <input 
                        type="search"
                        placeholder="Enter your XQuery"
                        v-model="state.query"
                    />
                    <button @click="runQuery">Run Query</button>   
                </div>
                <!-- Start & Count Inputs -->
                <div class="pagination-controls">
                    <label for="start">Start:</label>
                    <input type="number" id="start" v-model="state.start" min="1" max="20571">

                    <label for="count">Count:</label>
                    <input type="number" id="count" v-model="state.count" min="1" max="100">
                </div>
            </div>
            
            <div v-if="state.error" class="alert alert-danger mt-3">
                {{ state.error }}
            </div>
            
            <div class="results-section mt-3">
                <h2>Results</h2>
                <div v-if="!state.isLoading">
                     <pre>{{ state.results }}</pre>
            </div>
                <div v-else>
                    Loading...
                </div>
            </div>
        </main>
    </div>

    <div>
      <Footer />
    </div>

</template>
