<script setup>
import SearchFields from '@/components/SearchFields.vue';
import SearchResults from '@/components/SearchResults.vue';
import cursiveLatin from '@/assets/images/sample.png';
import { onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';

const state = reactive({
    displayResults: false,
    queryParams: []
});

const isValidQuery = (params) => {
    return true
}


onMounted(() => {
    const route = useRoute();
    const queryParams = route.query;
    console.log("query num:", Object.keys(queryParams).length);
    const hasQueryParams = Object.keys(queryParams).length > 0;
    if (hasQueryParams && isValidQuery(queryParams)){
        state.displayResults = true;
        state.queryParams = queryParams;
    }
    console.log(state.displayResults);
});
// console.log(props.queryParams);
</script>

<template>
    
    <div>

        <!-- Main Section -->
        <div>
            <SearchFields />
            <div v-if="state.displayResults">
                <SearchResults :queryParams="state.queryParams"/>
            </div>
        </div>

    </div>
</template>
