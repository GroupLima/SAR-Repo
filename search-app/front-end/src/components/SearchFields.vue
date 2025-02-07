<!-- view for all the search fields, and running the query with the given user input -->
<script setup>
import router from '@/router';
import { reactive, ref, toRaw } from 'vue';

const form = reactive({
    query_type: "basic_search",
    basicSearch: "holly",
    methodSearch: "word_start", // default type of string matching for basic search
    language: "any",
    variant: "0",
    volumes: [],
    pageSearch: "",
    entrySearch: "",
    startDate: "",
    endDate: "",
    docId: ""
});

const isDropdownOpen = ref(false); // don't display dropdown initally

const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value;
}

const passFormValues = () => {
    const rawForm = toRaw(form);
    const queryParams = new URLSearchParams(form).toString(rawForm);
    console.log(queryParams);
    router.push({ path: '/search', query: rawForm }); 
}

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

    return query_type
}

const handleSearch = () => {
    
    if (allValidInput){
        
        form.query_type = getSearchType();
        // const queryParams = {
        //     query_type: searchType,
        //     basicSearch: searchType,
        //     methodSearch: "starts with", // default type of string matching for basic search
        //     language: "any",
        //     variant: "",
        //     volumes: [],
        //     pageSearch: "",
        //     entrySearch: "",
        //     startDate: "",
        //     endDate: "",
        //     docId: ""
        // };
        try {
            passFormValues();
            
        } catch (error){
            console.error("error with search form", error);
        }
    }
}

const allValidInput = () => {
    //return true if all inputs are valid
    //return false otherwise and apply appropriate action

    return true //remove once implemented
}

</script>

<template>
    <div>

        <!-- SASS people please read!
        I have used IDs, rather than classes, to identify each form option, because the purpose of ids is to identify single, unique elements.
        Hopefully its enough so that the search class people can link it all together.
        Classes are for grouping multiple elements together so i used them to identify areas that might have similar styling and behaviour to
        each other. -->
        <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>

        <div class="search-section">
            <div class="basic-search"> <!-- this is the basic search bar -->
                <input type="search" v-model="form.basicSearch" placeholder="Enter your search term" aria-label="Search" id="search-box"/>
                <!-- we need something that looks like a button here: "SEARCH"-->
                <button id="search-button" @click="handleSearch">
                    SEARCH
                </button>
                <!-- need constriction so that user cannot search with empty bar -->
            </div>
            <div id="advanced" class="advanced-search-container"> <!-- form for advanced filters -->
                <button class="dropdown-button" @click="toggleDropdown">
                    ADVANCED SEARCH ▼
                </button>
                <div v-if="isDropdownOpen" class="advanced-search-dropdown">
                    <div id="search-options">
                        <div id="search-methods-radio" class="advanced-option">
                            <h3 class="option-title">Search Method</h3>
                            <label>
                                <input type="radio" v-model="form.methodSearch" value="keywords" id="keywords"
                                    name="search-method"> Keywords
                            </label>
                            <label>
                                <input type="radio" v-model="form.methodSearch" value="phrase" id="phrase" name="search-method">
                                Phrase
                            </label>
                            <label>
                                <input type="radio" v-model="form.methodSearch" value="regex" id="regularex"
                                    name="search-method"> Regular
                                Expression
                            </label>
                            <label>
                                <input type="radio" v-model="form.methodSearch" value="word_start" id="word-start"
                                    name="search-method" checked> Word
                                Start
                            </label>
                            <label>
                                <input type="radio" v-model="form.methodSearch" value="word_middle" id="word-middle"
                                    name="search-method"> Word
                                Middle
                            </label>
                            <label>
                                <input type="radio" v-model="form.methodSearch" value="word_end" id="word-end"
                                    name="search-method"> Word End
                            </label>
                        </div>
                        <div class="advanced-option">
                            <h3 class="option-title">Languages</h3>
                            <select v-model="form.language" id="language">
                                <option value="any" selected>Any</option>
                                <option value="latin">Latin</option>
                                <option value="scots">Middle Scots</option>
                                <option value="dutch">Dutch</option>
                            </select>
                        </div>
                        <div class="advanced-option">
                            <h3 class="option-title">Spelling Variants</h3>
                            <select v-model="form.variant" id="variant">
                                <option value="0" selected>0</option>
                                <option value="1">1</option>
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>
                            </select>
                        </div>
                        <div id=volume-select class="advanced-option">
                            <!-- Maybe a toggle button to automatically select all would be good-->
                            <h3 class="option-title">Volume</h3>
                            <label>
                                <input type="checkbox" v-model="form.volumes" id="volume-1" name="volume1" value="1"> 1
                            </label>
                            <label>
                                <input type="checkbox" v-model="form.volumes" id="volume-2" name="volume2" value="2"> 2
                            </label>
                            <label>
                                <input type="checkbox" v-model="form.volumes" id="volume-4" name="volume4" value="4"> 4
                            </label>
                            <label>
                                <input type="checkbox" v-model="form.volumes" id="volume-5" name="volume5" value="5"> 5
                            </label>
                            <label>
                                <input type="checkbox" v-model="form.volumes" id="volume-6" name="volume6" value="6"> 6
                            </label>
                            <label>
                                <input type="checkbox" v-model="form.volumes" id="volume-7" name="volume7" value="7"> 7
                            </label>
                            <label>
                                <input type="checkbox" v-model="form.volumes" id="volume-8" name="volume8" value="8"> 8
                            </label>
                        </div>
                        <!-- We need a constraint to restrict between 1 and the max page number -->
                        <div class="advanced-option">
                            <h3 class="option-title">Page Search</h3>
                            <input type="search" v-model="form.pageSearch" id="page-search" placeholder="1, 69, 591...">
                        </div>
                        <!-- We need a constraint to restrict between 1 and the number of entries -->
                        <div class="advanced-option">
                            <h3 class="option-title">Entry</h3>
                            <input type="search" v-model="form.entrySearch" id="entry-search" placeholder="1, 2, 3, 4...">
                        </div>
                        <!-- We need to apply constraints to limit date between 1398 and 1510 -->
                        <div id="dates" class="option-title">
                            <h3 class="option-title">Date Range</h3>
                            <label>
                                from <input type="date" v-model="form.startDate" id="start-date" name="start-date">
                            </label>
                            <label>
                                to <input type="date" v-model="form.endDate" id="end-date" name="end-date">
                            </label>
                        </div>
                        <!-- We should only allow valid DocIDs -->
                        <div class="advanced-option">
                            <h3 class="option-title">Doc ID</h3>
                            <input type="search" v-model="form.docId" id="doc-id-search" placeholder="ARO-1-0001-01">
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>