<script setup>
import SearchFields from '@/components/SearchFields.vue';
import Footer from '@/components/Footer.vue';
// console.log(props.queryParams);
</script>

<template>
    <div class="home-page">
        <!-- Header Section -->
        <header>
            <div class="home-description">
                <h1>Discover 8 Volumes</h1>
                <p>Some text explaining search</p>
            </div>
        </header>
        <!-- Main Section -->
        <main>
            <div>
                <SearchFields />
            </div>
        </main>
    </div>
    <!-- Footer Section -->
    <div>
        <Footer />
    </div>
</template>
