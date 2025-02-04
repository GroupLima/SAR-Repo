<script setup>
import SearchFields from '@/components/SearchFields.vue';
import cursiveLatin from '@/assets/images/sample.png';


// console.log(props.queryParams);
</script>

<template>
    
    <div>
         <!-- Header Section -->
        <header>
            <div class="header-content"></div>
        </header>

        <!-- Main Section -->
        <div class="aro-description">Discover 8 Volumes</div>
        <p>Some text explaining search</p>
        <div>
            <SearchFields />
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
