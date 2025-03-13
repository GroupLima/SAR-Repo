<script setup>
import { useDark } from '@vueuse/core'
const isDark = useDark({selector: 'body'})
</script>

<template>
  <footer>
    <div class="image-container">
      <img v-if="isDark" src="@/assets/images/new-scripture-dark.png" alt="Cursive Latin" />
      <img v-else src="@/assets/images/new-scripture.png" alt="Cursive Latin" />
    </div>
    <div class="footer-links-container">
      <div class="footer-links">
        <a href="https://www.abdn.ac.uk/aro" target="_blank">Aberdeen Registers Online</a>
        <a href="https://sar.abdn.ac.uk/" target="_blank">Old Website</a>
        <a href="https://www.abdn.ac.uk/" target="_blank">Aberdeen University</a>
        <a href="https://github.com/GroupLima" target="_blank">Our GitHub</a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.image-container img {
  object-fit: cover; /* Ensure the image fits within the container without stretching */
  width: 100%;
  height: auto;
}

.footer-links-container {
  padding: 10px; /* Adjust padding for smaller screens */
}

.footer-links {
  flex-direction: column; /* Stack links vertically on smaller screens */
  align-items: center;
}
</style>