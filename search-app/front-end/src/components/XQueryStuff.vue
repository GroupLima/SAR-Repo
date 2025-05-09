<script setup>
import { reactive, onMounted } from 'vue';
import axios from 'axios';
import vkbeautify from 'vkbeautify';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css'; // ADDED CSS
import 'highlight.js/styles/github-dark.css';
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
  num_results: 0,
  total_results: 0,
  error: "",
  isLoading: false
});

const runQuery = async () => {
  const XQueryURL = '/api/xquery' // FIXED TYPO IN VARIABLE NAME
  state.isLoading = true;
  state.results = '';
  state.error = "";

  try {
    const response = await axios.get(XQueryURL, {
      params: {
        query_type: "xquery",
        query: state.query,
      },
    });

    if (response.data.success) {
      const xmlString = response.data.queryResults;
      const xmlPretty = vkbeautify.xml(xmlString, 5);
      
      // ADDED RESULTS HIGHLIGHTING
      state.results = hljs.highlight(xmlPretty, {
        language: 'xml',
        ignoreIllegals: true
      }).value;
      
    } else {
      state.error = "No results found!";
    }
  } catch (error) {
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
        <h2>Results</h2>
        <div v-if="!state.isLoading">
          <!-- CHANGED RESULTS DISPLAY -->
          <pre v-if="state.results"><code class="hljs language-xml" v-html="state.results"></code></pre>
        </div>
        <!-- <div v-else>
          Loading...
        </div> -->
        <div class="loading-spinner-container">
                <div class="loading-spinner"></div>
            </div>
      </div>
    </main>
  </div>
</template>

<!-- ADD THESE STYLES --><style scoped>
.xquery-page {
  .results-section {
    .hljs {
      padding: 1rem;
      border-radius: 4px;
      background-color: #ffffff;
      color: #000000;
      transition: all 0.3s;

      /* 

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
  }
}
</style>