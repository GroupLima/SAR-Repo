<script setup>
import SearchFields from '@/components/SearchFields.vue';
import Footer from '@/components/Footer.vue';
// console.log(props.queryParams);
</script>

<template>
    
    <div>
         <!-- Header Section -->
        <header>
            <div class="header-content"></div>
        </header>

        <!-- Main Section -->
        <div class="aro-description">
            <h1>Discover 8 Volumes</h1>
            <p>Some text explaining search</p>
        </div>
        <div>
            <SearchFields />
        </div>

        <div>
            <Footer />
        </div>

    </div>
</template>
