<script setup>
import SearchFields from '@/components/SearchFields.vue';
// console.log(props.queryParams);
</script>

<template>
    <div class="home-page">
        <!-- Header Section -->
        <header>
            <div class="home-description">
                <h1>Discover 7 Volumes</h1>
                <br>
                <p><b>Search Aberdeen Registers</b> is a digital tool that allows you to explore the rich historical records of Aberdeen’s burgh registers. These records date back to the 16th century and offer a unique insight into the city’s legal, social, and economic history. Whether you're a researcher, student, or history enthusiast, this tool makes it easy to search, discover, and learn from Aberdeen’s past.</p>
                <br>
            </div>
        </header>
        <!-- Main Section -->
        <main>
            <div>
                <SearchFields />
            </div>
        </main>
    </div>
</template>
