<script setup>
import { RouterLink } from 'vue-router';
import { useDark, useToggle } from '@vueuse/core'
import { inject, computed, ref } from 'vue';
const isDark = useDark({selector: 'body'})
const toggleDark = useToggle(isDark);

const selectedRecords = inject('selectedRecords');
const hasSelectedRecords = computed(() => selectedRecords.value.length > 0);

const isMenuOpen = ref(false);
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

// Adds class scrolled when y position > 50
window.onscroll = function() {
    var navbar = document.querySelector(".navbar");
    if (window.scrollY > 30) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }
}
</script>

<template>
    <nav class="navbar">
        <div class="nav-content">
            <RouterLink to="/" class="logo-section">
                <div class="text-container">
                    <img src="@/assets/images/logo-current.png" alt="SAR Logo"/>
                </div>
            </RouterLink>
            <div class="burger-menu" @click="toggleMenu">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <div :class="['nav-links', { active: isMenuOpen }]">
                <RouterLink to="/">Home</RouterLink>
                <RouterLink to="/browse">Browse</RouterLink>
                <RouterLink to="/xQuery">XQuery</RouterLink>
                <RouterLink to="/about">About</RouterLink>
                <RouterLink to="/help" class="help-link">Help</RouterLink>
                <RouterLink v-if="hasSelectedRecords" to="/selected">
                Selected ({{ selectedRecords.length }})
                </RouterLink>
                <button
                    class="dark-mode-button"
                    type="button"
                    @click="toggleDark()">
                    <div v-if="isDark"><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-280q-83 0-141.5-58.5T280-480q0-83 58.5-141.5T480-680q83 0 141.5 58.5T680-480q0 83-58.5 141.5T480-280ZM200-440H40v-80h160v80Zm720 0H760v-80h160v80ZM440-760v-160h80v160h-80Zm0 720v-160h80v160h-80ZM256-650l-101-97 57-59 96 100-52 56Zm492 496-97-101 53-55 101 97-57 59Zm-98-550 97-101 59 57-100 96-56-52ZM154-212l101-97 55 53-97 101-59-57Z"/></svg></div>
                    <div v-else><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-120q-150 0-255-105T120-480q0-150 105-255t255-105q14 0 27.5 1t26.5 3q-41 29-65.5 75.5T444-660q0 90 63 153t153 63q55 0 101-24.5t75-65.5q2 13 3 26.5t1 27.5q0 150-105 255T480-120Z"/></svg></div>
                </button>
            </div>
        </div>
    </nav>
</template>

<script>
import router from '@/router';

export default {
  name: 'Navbar',
  methods: {
    showHelp() {
      const routeUrl = router.resolve({ name: 'help' }).href;
      window.open(routeUrl, '_blank');
    }
  }
};
</script>
