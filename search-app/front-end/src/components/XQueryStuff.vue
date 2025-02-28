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
    isLoading: false
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
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <div class="container">
        <header>
            <div class="header-content">
                <h1>XQuery Search</h1>
                <p>Search through XML documents using XQuery</p>
            </div>
        </header>
        
        <main>
            <div class="search-section">
                <input 
                    type="search"
                    placeholder="Enter your XQuery"
                    v-model="state.query"
                />
                <button @click="runQuery">Run Query</button>   
            </div>
            
            <div v-if="state.error" class="alert alert-danger mt-3">
                {{ state.error }}
            </div>
            
            <div class="results-section mt-3">
                <h2 class="results-title">Results</h2>
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
