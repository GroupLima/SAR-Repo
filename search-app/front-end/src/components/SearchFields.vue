<script setup>
import router from '@/router';
import { reactive, ref, toRaw, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router'; // Import the useRoute hook
import DatePicker from '@/components/DatePicker.vue';


const route = useRoute();

const dateFrom = ref();
const dateTo = ref();

const form = reactive({
    query_type: "basic_search",
    basicSearch: "",
    methodSearch: "word_start", // default type of string matching for basic search
    language: "any",
    variant: "0",
    volumes: [],
    pageSearch: "",
    entrySearch: "",
    startDate: "",
    endDate: "",
    docId: "",
    resultsPerPage: 10,
    sortBy: "Frequency within result"
});

const isDropdownOpen = ref(false); // don't display dropdown initially

const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value;
};

const passFormValues = () => {
    const rawForm = toRaw(form);
    const queryParams = new URLSearchParams(form).toString(rawForm);
    console.log(queryParams);
    router.push({ path: '/search', query: rawForm }).then(() => {
        window.location.reload();
    });
};

const getSearchType = () => {
    const query_type = 
    form.language !== "any" || 
    form.volumes.length > 0 || 
    form.pageSearch !== "" || 
    form.entrySearch !== "" ||
    form.startDate !== "" ||
    form.endDate !== "" ||
    form.docId !== ""
    ? "advanced_search"  //select advanced search if at least one of the advanced search fields is filled out
    : "basic_search";

    return query_type;
};

const isAllSelected = computed(() => {
    return form.volumes.length === 7;
});

const toggleAllVolumes = () => {
    if (isAllSelected.value) {
        form.volumes = [];
    } else {
        form.volumes = ['1', '2', '4', '5', '6', '7', '8'];
    }
};

const handleSearch = () => {
    if (allValidInput()) {
        form.query_type = getSearchType();
        try {
            if (form.basicSearch.trim() === "") {
                form.basicSearch = ".*" // allow searching though all docs with no query
            }
            passFormValues();
        } catch (error) {
            console.error("error with search form", error);
        }
    }
};

const allValidInput = () => {
    //return true if all inputs are valid
    //return false otherwise and apply appropriate action
    const searchType = getSearchType();
    
    // if basic search, require a non-empty search bar input
    if (searchType === "basic_search" && form.basicSearch.trim() === "") {
        alert("Please enter a query in the search bar or select an Advanced Search option");
        return false;
    }
    if (form.startDate != "" && !validDate("startDate")){
        alert("Please enter a valid 'From' date");
        return false;
    }
    if (form.endDate !="" && !validDate("endDate")){
        alert("Please enter a valid 'To' date");
        return false;
    }
    return true; //remove once implemented
};

const validDate = (dateField) => {
    // check that numbers in date are valid
    const parts = form[dateField].split("-");
    let dateLength = 0;
    for (let i = 0; i < 3; i++) {
        const part = parts[i];
        if (!part || part === "undefined" || !/^\d+$/.test(part)) break;

        dateLength++;
    }
    if (dateLength > 0){
        form[dateField] = parts.slice(0, dateLength).join("-");
        return true;
    }
    return false;
};



const handleEnterKey = (event) => {
    if (event.key === 'Enter') {
        handleSearch();
    }
};

const setSearchBoxValue = () => {
    const urlParams = new URLSearchParams(window.location.search);
    form.basicSearch = urlParams.get('basicSearch') || form.basicSearch;
    form.methodSearch = urlParams.get('methodSearch') || form.methodSearch;
    form.language = urlParams.get('language') || form.language;
    form.variant = urlParams.get('variant') || form.variant;
    form.volumes = urlParams.getAll('volumes') || form.volumes;
    form.pageSearch = urlParams.get('pageSearch') || form.pageSearch;
    form.entrySearch = urlParams.get('entrySearch') || form.entrySearch;
    form.startDate = urlParams.get('startDate') || form.startDate;
    form.endDate = urlParams.get('endDate') || form.endDate;
    form.docId = urlParams.get('docId') || form.docId;
    form.resultsPerPage = Number(route.query.resultsPerPage) || form.resultsPerPage;
};

const resetAdvancedSearch = () => {
    form.methodSearch = "word_start";
    form.language = "any";
    form.variant = "0";
    form.volumes = [];
    form.pageSearch = "";
    form.entrySearch = "";
    form.startDate = "";
    dateFrom.value?.clearInput();
    form.endDate = "";
    dateTo.value?.clearInput();
    form.docId = "";
};

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

onMounted(() => {
    setSearchBoxValue();
});

</script>

<template>
    <div>

        <!-- SASS people please read!
        I have used IDs, rather than classes, to identify each form option, because the purpose of ids is to identify single, unique elements.
        Hopefully its enough so that the search class people can link it all together.
        Classes are for grouping multiple elements together so i used them to identify areas that might have similar styling and behaviour to
        each other. -->

        <div class="search-section">
            <div class="basic-search"> <!-- this is the basic search bar -->
                <input type="search" v-model="form.basicSearch" placeholder="Enter your search term" aria-label="Search" id="search-box" @keyup="handleEnterKey"/>
                <!-- we need something that looks like a button here: "SEARCH"-->
                <button id="search-button" @click="handleSearch">
                    SEARCH
                </button>
                <!-- need constriction so that user cannot search with empty bar -->
            </div>
            <div class="preferences" style="text-align: center;">
                <div class="preference-item">
                    <label>Search method:</label>
                    <select v-model="form.methodSearch">
                        <option v-for="sm in searchMethods" :key="sm.value" :value="sm.value">{{ sm.text }}</option>
                    </select>
                </div>
                <div class="preference-item">
                    <label>Variants:</label>
                    <select v-model="form.variant">
                        <option v-for="variant in varOptions" :key="variant" :value="variant">{{ variant }}</option>
                    </select>
                </div>
                <div class="preference-item">
                    <label>Results per page:</label>
                    <select v-model="form.resultsPerPage">
                        <option v-for="rpp in rrpOptions" :key="rpp" :value="rpp">{{ rpp }}</option>
                    </select>
                </div>
                <div class="preference-item">
                    <label>Sort by:</label>
                    <select v-model="form.sortBy">
                        <option v-for="ord in ordOptions" :key="ord" :value="ord">{{ ord }}</option>
                    </select>
                </div>
            </div>
            <div id="advanced" class="advanced-search-container"> <!-- form for advanced filters -->
                <button class="dropdown-button" @click="toggleDropdown">
                    ADVANCED SEARCH
                    <span class="dropdown-arrow" :class="{ 'open': isDropdownOpen }">▼</span>
                </button>
                <div v-if="isDropdownOpen" class="advanced-search-dropdown">
                    <div id="search-options">
                        <!-- Removed title and radio buttons from advanced search drop-down -->
                        <div class="advanced-option">
                            <h3 class="option-title">Languages</h3>
                            <select v-model="form.language" id="language">
                                <option value="any" selected>Any</option>
                                <option value="latin">Latin</option>
                                <option value="scots">Middle Scots</option>
                                <option value="dutch">Dutch</option>
                                <option value="multiple">Multiple</option>
                            </select>
                        </div>
                        <!-- <div class="advanced-option">
                            <h3 class="option-title">Spelling Variants</h3>
                            <select v-model="form.variant" id="variant">
                                <option value="0" selected>0</option>
                                <option value="1">1</option>
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>
                            </select>
                        </div> -->
                        <div id="volume-select" class="advanced-option">
                            <h3 class="option-title">Volume</h3>
                            <div class="horizontal-list">
                                <label v-for="volume in ['1', '2', '4', '5', '6', '7', '8']" :key="volume">
                                    <input type="checkbox" v-model="form.volumes" :id="volume" :value="volume"> {{ volume }}
                                </label>
                                <label>
                                    <input type="checkbox" :checked="isAllSelected" @change="toggleAllVolumes"> All
                                </label>
                            </div>
                        </div>
                        <!-- We need a constraint to restrict between 1 and the max page number -->
                        <div class="advanced-option">
                            <h3 class="option-title">Page Search</h3>
                            <input type="search" v-model="form.pageSearch" id="page-search" placeholder="1, 69, 591...">
                        </div>
                        <!-- We need a constraint to restrict between 1 and the number of entries -->
                        <div class="advanced-option" style="display: none;">
                            <h3 class="option-title">Entry</h3>
                            <input type="search" v-model="form.entrySearch" id="entry-search" placeholder="1, 2, 3, 4...">
                        </div>
                        <!-- We need to apply constraints to limit date between 1398 and 1510 -->
                        <div id="dates" class="option-title">
                            <h3 class="option-title">Date Range</h3>
                            <label>
                                From: <DatePicker ref="dateFrom" v-model="form.startDate" id="start-date" name="start-date" :yearAscending="true"/>
                            </label>
                            <label>
                                To: <DatePicker ref="dateTo" v-model="form.endDate" id="end-date" name="end-date"/>
                            </label>
                        </div>
                        <!-- We should only allow valid DocIDs -->
                        <div class="advanced-option">
                            <h3 class="option-title">Doc ID</h3>
                            <input type="search" v-model="form.docId" id="doc-id-search" placeholder="ARO-1-0001-01">
                        </div>
                        <div class="advanced-option">
                            <button @click="resetAdvancedSearch" class="reset-button">Reset Field Values</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>