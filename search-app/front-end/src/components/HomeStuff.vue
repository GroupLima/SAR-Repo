<script setup>
import SearchFields from '@/components/SearchFields.vue';
import Footer from '@/components/Footer.vue';
// console.log(props.queryParams);
</script>

<template>
    <div>
        <!-- Header Section -->
        <header>
            <div class="header-content">
                <h1>Discover 8 Volumes</h1>
                <p>Some text explaining search</p>
            </div>
        </header>

        <!-- Main Section -->
        <div>
            <SearchFields />
        </div>

        <!-- Footer Section -->
        <div>
            <Footer />
        </div>
    </div>
</template>
