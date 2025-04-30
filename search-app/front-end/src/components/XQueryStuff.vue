<script setup>
import { reactive, onMounted } from 'vue';
import axios from 'axios';
import vkbeautify from 'vkbeautify';

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
    isLoading: false
});

const handleEnterKey = (event) => {
    if (event.key === 'Enter') {
        runQuery();
    }
};

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
            },
        });
        console.log("Response received:", response);
        if (response.data.message) {
            // Directly map response to state.results
            const xmlString = response.data.message.queryResults;
            console.log(typeof xmlString, xmlString);
            const xmlPretty = vkbeautify.xml(xmlString, 5);
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
                <h1>XQuery Search</h1>
                <br/>
                <p>Harness the power of XQuery to perform precise, structured searches across our collection of XML-encoded historical documents. This advanced search tool allows you to craft custom queries that target specific elements, attributes, and content patterns within the document corpus.</p>
            </div>
        </header>
        
        <main class="content">
            <div class="search-section">
                <div class="basic-search">
                    <input 
                        type="search" v-model="state.query" placeholder="Enter your search term" id="search-box" @keyup="handleEnterKey"
                    />
                    <button @click="runQuery">Run Query</button>   
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
</template>