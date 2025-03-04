
<script setup>
import { RouterView } from 'vue-router'
import { ref, provide } from 'vue'
import Navbar from './components/Navbar.vue';
import UserManual from './components/UserManual.vue';

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
      <UserManual/>
    </div>
  </div>
</template>