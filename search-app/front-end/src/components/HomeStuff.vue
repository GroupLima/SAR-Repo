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
                <a href="https://www.abdn.ac.uk/aro" target="_blank">Aberdeen Registers Online</a>
                <a href="https://sar.abdn.ac.uk/" target="_blank">Old Website</a>
                <a href="https://www.abdn.ac.uk/" target="_blank">University Page</a>
                <a href="https://github.com/GroupLima" target="_blank">About Us</a>
            </div>
        </footer>

    </div>
</template>
