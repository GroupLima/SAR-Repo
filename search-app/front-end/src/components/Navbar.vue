<script setup>
import { RouterLink } from 'vue-router';
import townLogo from '@/assets/images/town.png';
</script>

<template>
    <nav id="navbar" class="navbar">
  <div class="nav-content">
    <div class="logo-section" onclick="navigateToPage('/home');">


      <div class="text-container">
        <!-- New container for text -->
        <div class="logo-text">SAR</div>
        <div class="logo-subtext">Search Aberdeen Registers</div>
      </div>
      <img :src="townLogo" alt="Town Logo" class="logo-image">
    </div>
    <div class="nav-links">
        <RouterLink to="/home">
            Home
        </RouterLink>
        <RouterLink to="/browse">
            Browse
        </RouterLink>
        <RouterLink to="/xquery">
            Xquery
        </RouterLink>
        <RouterLink to="/about">
            About
        </RouterLink>
      <!-- <a href="/home" onclick="navigateToPage('/home'); return false;">Home</a>
      <a href="/browse" onclick="navigateToPage('/browse'); return false;">Browse</a>
      <a href="/xquery" onclick="navigateToPage('/xquery'); return false;">XQuery</a>
      <a href="/about" onclick="navigateToPage('/about'); return false;">About</a> -->
    </div>
  </div>
</nav>
</template>