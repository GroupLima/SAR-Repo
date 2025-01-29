<script setup>
import { RouterLink } from 'vue-router';
import townLogo from '@/assets/images/town.png';

</script>

<template>
    <nav id="navbar" class="navbar">
        <div class="nav-content">
            <RouterLink to="/" class="logo-section">
                <div class="text-container">
                    <!-- New container for text -->
                    <div class="logo-text">SAR</div>
                    <div class="logo-subtext">Search Aberdeen Registers</div>
                </div>
                <img :src="townLogo" alt="Town Logo" class="logo-image">
            </RouterLink>
            <div class="nav-links">
                <RouterLink to="/">
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
            </div>
        </div>
    </nav>
</template>