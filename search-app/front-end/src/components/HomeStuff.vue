<script setup>
import SearchFields from '@/components/SearchFields.vue';
import Footer from '@/components/Footer.vue';
// console.log(props.queryParams);
</script>

<template>
    <div>
        <!-- Main Section -->
        <main>
            <div class="home-description">
                <h1>Discover 8 Volumes</h1>
                <p>Some text explaining search</p>
            </div>
            <div>
                <SearchFields />
            </div>
        </main>
        <!-- Footer Section -->
        <div>
            <Footer />
        </div>
    </div>
</template>
