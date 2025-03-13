<script setup>
import { RouterView } from 'vue-router'
import { ref, provide } from 'vue'
import Navbar from './components/Navbar.vue';
import HelpPage from './components/HelpPage.vue';
import Footer from '@/components/Footer.vue';

const selectedRecords = ref([]);
provide('selectedRecords', selectedRecords);
</script>

<template>
  <div >
    <Navbar/>
    <div>
      <RouterView />
    </div>
    <div>
      <HelpPage/>
    </div>
  </div>
  <div>
      <Footer />
  </div>
</template>