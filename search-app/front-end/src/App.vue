
<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div >
    <Navbar class="example"/>
    <div>
      <RouterView />
    </div>
  </div>
</template>

<style scope>
.example {
  background: #6e0d25;
}
</style>