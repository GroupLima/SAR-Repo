<script setup>
import { reactive, onMounted, computed } from 'vue';
import axios from 'axios';
import vkbeautify from 'vkbeautify';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css'; // ADDED CSS
import 'highlight.js/styles/github-dark.css';
import 'highlight.js/styles/atom-one-light.css';
import CodeEditor from "simple-code-editor";
import { useDark } from '@vueuse/core'
const isDark = useDark({selector: 'body'})


// ADDED HIGHLIGHT SETUP
const highlightCode = (code) => {
  return hljs.highlight(code, { language: 'xquery' }).value;
};

onMounted(() => {
  hljs.configure({ languages: ['xml', 'xquery'] });
});

const props = defineProps({
  queryParams: {
    type: Object,
    required: true
  }
});

const state = reactive({
  query: '',
  results: '',
  rawResults: null, // Store the raw XML string
  processedResults: [], // Store the processed results for pagination
  currentPage: 1,
  pageSize: 20, // Number of results to display per page
  totalResults: 0,
  totalPages: 1,
  error: "",
  isLoading: false,
  isFirstLoad: true, // Flag to handle initial empty state
  queryId: null, // To track query execution on server
  isFetchingPage: false // Flag to track pagination loading
});

// Computed property for current page items
const currentPageItems = computed(() => {
  if (!state.processedResults.length) return [];
  
  const start = (state.currentPage - 1) * state.pageSize;
  const end = start + state.pageSize;
  return state.processedResults.slice(start, end);
});

// Function to navigate to a specific page
const goToPage = (page) => {
  if (page >= 1 && page <= state.totalPages) {
    // If we have all results already loaded in memory, just render the requested page
    if (state.processedResults.length === state.totalResults) {
      state.currentPage = page;
      renderCurrentPage();
    } else {
      // Otherwise fetch the specific page from the server
      fetchPage(page);
    }
  }
};

// Function to render the current page of results
const renderCurrentPage = () => {
  if (!currentPageItems.value.length) return;
  
  // Join the current page items and format them
  const pageContent = currentPageItems.value.join('\n');
  const xmlPretty = vkbeautify.xml(pageContent, 5);
  
  // Highlight the XML
  state.results = hljs.highlight(xmlPretty, {
    language: 'xml',
    ignoreIllegals: true
  }).value;
};

// Process XML results to enable pagination
const processResults = (xmlString) => {
  // Store the raw XML
  state.rawResults = xmlString;
  
  try {
    // Parse the XML to extract individual item elements
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlString, "text/xml");
    
    // Get the count of results
    const countElement = xmlDoc.querySelector("count");
    state.totalResults = countElement ? parseInt(countElement.textContent) : 0;
    
    // Get all item elements (divs or whatever your XQuery returns)
    const temp_items = Array.from(xmlDoc.querySelectorAll("items > div"));

    let items; // declare outside the if/else so it's in scope

    if (temp_items.length === 0) {
      // No <div>s — use the <items> element itself
      items = Array.from(xmlDoc.querySelectorAll("items"));
    } else {
      items = temp_items;
    }

    console.error("itmes:", items);
    // Convert each item to its XML string representation
    state.processedResults = items.map(item => {
      const serializer = new XMLSerializer();
      return serializer.serializeToString(item);
    });
    
    // Calculate total pages
    state.totalPages = Math.ceil(state.processedResults.length / state.pageSize);
    
    // Set to page 1 and render
    state.currentPage = 1;
    renderCurrentPage();
    
  } catch (error) {
    console.error("Error processing XML results:", error);
    state.error = "Error processing results. XML may be malformed.";
    state.results = '';
  }
};

// Fetch a specific page of results
const fetchPage = async (page) => {
  if (!state.queryId) return;
  
  state.isFetchingPage = true;
  try {
    const response = await axios.get('/api/xquery', {
      params: {
        query_type: "xquery_page",
        queryId: state.queryId,
        page: page,
        pageSize: state.pageSize
      },
      timeout: 30000
    });

    if (response.data.success) {
      const xmlString = response.data.queryResults;
      
      // Just update the current view, don't reprocess all results
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlString, "text/xml");
      
      // Get items for this page
      const items = Array.from(xmlDoc.querySelectorAll("items > div"));
      
      // Convert each item to its XML string representation
      const pageItems = items.map(item => {
        const serializer = new XMLSerializer();
        return serializer.serializeToString(item);
      });
      
      // Create a partial XML string for rendering
      const pageContent = pageItems.join('\n');
      const xmlPretty = vkbeautify.xml(pageContent, 5);
      console.log("XML STRING RECEIVED:", xmlPretty); // <-- AND THIS
      
      // Highlight the XML
      state.results = hljs.highlight(xmlPretty, {
        language: 'xml',
        ignoreIllegals: true
      }).value;
      
      state.currentPage = page;
    } else {
      console.error("Error fetching page:", response.data);
    }
  } catch (error) {
    console.error("Error fetching page:", error);
  } finally {
    state.isFetchingPage = false;
  }
};

const runQuery = async () => {
  console.log("Running query...")
  const XQueryURL = '/api/xquery' // FIXED TYPO IN VARIABLE NAME
  state.isLoading = true;
  state.results = '';
  state.error = "";
  state.isFirstLoad = false;
  
  try {
    const response = await axios.get(XQueryURL, {
      params: {
        query_type: "xquery",
        query: state.query,
        page: 1,
        pageSize: state.pageSize
      },
      timeout: 60000 // Increase timeout to 60 seconds for complex queries
    });
    console.log("RESPONSE:", response.data);
    if (response.data.success) {
      // Store query ID for subsequent page requests
      state.queryId = response.data.queryId || null;
      state.totalResults = response.data.totalResults || 0;
      state.totalPages = response.data.totalPages || 1;
      
      const xmlString = response.data.queryResults;
      processResults(xmlString);
    } else {
      state.error = "No results found!";
    }
  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      state.error = "Query timed out. Please try a more specific query.";
    } else {
      state.error = error.response?.data?.error || 'An unexpected error occurred';
    }
    console.error('XQuery error:', error);
  } finally {
    state.isLoading = false;
  }
};

// Download full results as XML
const downloadResults = () => {
  if (!state.rawResults) return;
  
  const blob = new Blob([state.rawResults], { type: 'application/xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'xquery_results.xml';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
</script>

<template>
  <div class="xquery-page">
    <header>
      <div class="header-content">
        <h1>XQuery Search</h1>
        <br/>
        <p>Harness the power of XQuery to perform precise, structured searches across our collection...</p>
      </div>
    </header>
    <br/>
    <main class="content">
      <div class="search-section">
        <CodeEditor 
          v-model="state.query" 
          :languages="[['xquery', 'XQuery']]"
          :highlight="highlightCode"
          :line-nums="true"
          width="100%"
          :theme="isDark ? 'github-dark' : 'github'"
        />
        <div class="basic-search">
          <button @click="runQuery">Run Query</button>   
        </div>
      </div>
      
      <div v-if="state.error" class="alert alert-danger mt-3">
        {{ state.error }}
      </div>
      
      <div class="results-section mt-3">
        <div class="results-header">
          <h2>Results</h2>
          <div v-if="state.totalResults > 0" class="results-meta">
            <span>Showing {{ state.processedResults.length }} results</span>
            <button v-if="state.rawResults" class="download-btn" @click="downloadResults">
              Download Full XML
            </button>
          </div>
        </div>

        <div v-if="state.isLoading" class="loading-spinner-container">
          <div class="loading-spinner"></div>
        </div>

        <div v-else-if="!state.isFirstLoad && !state.results && !state.error" class="no-results">
          No results found
          
        </div>
        
        <template v-else>
          <!-- Results display -->
          <div v-if="state.isFetchingPage" class="loading-spinner-container">
            <div class="loading-spinner"></div>
            <div>Loading page {{ state.currentPage }}...</div>
          </div>
          
          <pre v-if="state.results && !state.isFetchingPage"><code class="hljs language-xml" v-html="state.results"></code></pre>
          
          <!-- Pagination controls -->
          <div v-if="state.totalPages > 1" class="pagination-controls">
            <button 
              :disabled="state.currentPage === 1 || state.isFetchingPage"
              @click="goToPage(state.currentPage - 1)"
              class="pagination-btn"
            >
              Previous
            </button>
            
            <span class="page-indicator">
              Page {{ state.currentPage }} of {{ state.totalPages }}
            </span>
            
            <button 
              :disabled="state.currentPage === state.totalPages || state.isFetchingPage"
              @click="goToPage(state.currentPage + 1)"
              class="pagination-btn"
            >
              Next
            </button>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<!-- ADD THESE STYLES -->
<style scoped>
.xquery-page {
  .results-section {
    .hljs {
      padding: 1rem;
      border-radius: 4px;
      background-color: #f7f7f7;
      color: #000000;
      transition: all 0.3s;

      /* Dark mode overrides */
      body.dark & {
        background-color: #2c2c2c;
        color: #e0e0e0;
      }
    }

    pre {
      margin: 0;
      background: transparent;
    }

    code {
      display: block;
      white-space: pre-wrap;
      font-family: 'Fira Code', monospace;
      line-height: 1.5;
    }
    
    .results-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      
      .results-meta {
        font-size: 0.9rem;
        color: #6c757d;
        display: flex;
        align-items: center;
        gap: 1rem;
      }
    }
    
    .no-results {
      text-align: center;
      padding: 2rem;
      color: #6c757d;
    }
    
    .pagination-controls {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-top: 1rem;
      gap: 1rem;
      
      .page-indicator {
        font-size: 0.9rem;
      }
      
      .pagination-btn {
        padding: 0.5rem 1rem;
        background-color: #6e0d25;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        
        &:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
        
        &:hover:not(:disabled) {
          background-color: #5a0a1e;
        }
      }
    }
    
    .download-btn {
      padding: 0.25rem 0.5rem;
      background-color: #6e0d25;
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 0.8rem;
      cursor: pointer;
      
      &:hover {
        background-color: #5a0a1e;
      }
    }
  }
  
  .loading-spinner-container {
    display: flex;
    justify-content: center;
    padding: 2rem 0;
  }
}
</style>
