<template>
    <div>
      <h2>Volume Selection</h2>
  
      <!-- "Select All" and "Deselect All" Buttons -->
      <button @click="selectAll" class="button">Select All Volumes</button>
      <button @click="deselectAll" class="button">Deselect All</button>
  
      <!-- Volume checkboxes -->
      <div class="volume-container">
        <label v-for="(vol, index) in volumes" :key="index">
          <input type="checkbox" v-model="selectedVolumes" :value="vol" class="volume-checkbox" />
          {{ vol }}
        </label>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        volumes: [1, 2, 3, 4, 5, 6, 7, 8], // Volume numbers
        selectedVolumes: [] // Holds selected volume numbers
      };
    },
    methods: {
      selectAll() {
        this.selectedVolumes = [...this.volumes]; // Select all volumes
      },
      deselectAll() {
        this.selectedVolumes = []; // Deselect all volumes
      }
    }
  };
  </script>
  
  <style scoped>
  @import '@/public/sass/app.css';
  </style>
  