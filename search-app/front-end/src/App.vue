
<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
import UserManual from './components/UserManual.vue';
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