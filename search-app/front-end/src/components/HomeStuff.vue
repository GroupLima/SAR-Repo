<script setup>
import SearchFields from '@/components/SearchFields.vue';
import SearchResults from '@/components/SearchResults.vue';
import cursiveLatin from '@/assets/images/sample.png';
import { defineProps } from 'vue';

const props = defineProps({
    displayResults: {
        type: Boolean,
        default: true
    },
    queryParams: []
});

</script>

<template>
    
    <div>
         <!-- Header Section -->
        <header>
        <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
            <div class="header-content">
                <div class="aro-description">Discover 8 Volumes</div>
            <p>Some text explaining search</p>
            <br><br>
            </div>
        </header>

        <!-- Main Section -->
        <div>
            <SearchFields />
            <div v-if="displayResults">
                <SearchResults :queryParams="queryParams"/>
            </div>
        </div>

        <div class="image-container">
            <img :src="cursiveLatin" alt="sample text" style="overflow: hidden;">
        </div> 

        <!-- Footer Section -->
        <footer>
            <div class="footer-links">
                <a href="#">IMPORTANT LINKS</a>
                <a href="#">BLOG PAGE</a>
                <a href="#">UNIVERSITY ARO PAGE</a>
                <a href="#">ACKNOWLEDGMENTS</a>
            </div>
        </footer>

    </div>
</template>
