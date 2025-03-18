<script setup>
import { RouterView } from 'vue-router'
import { ref, provide, watch } from 'vue'
import Navbar from './components/Navbar.vue';
import HelpPage from './components/HelpPage.vue';

// Initialize selectedRecords - Try to load from localStorage first
const savedRecords = localStorage.getItem('selectedRecords');
const selectedRecords = ref(savedRecords ? JSON.parse(savedRecords) : []);

// Save to localStorage whenever selectedRecords changes
watch(selectedRecords, (newValue) => {
  localStorage.setItem('selectedRecords', JSON.stringify(newValue));
}, { deep: true });

// Provide selectedRecords to all components
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
</template>