<script setup>
import router from '@/router';
import Footer from '@/components/Footer.vue';
</script>

<template>
  <div class="about-stuff">
    <div class="row">
      <div class="column">
        <h2>Aberdeen Burgh Registers</h2>
        <div class = "about-text">
          <br>
          <p>The Aberdeen Registers Online (ARO) corpus is a comprehensive digitised transcription of the first eight volumes of the Aberdeen Burgh Registers, the oldest surviving civic government records in Scotland. Spanning 113 years from 1398 (volume one) to 1511 (volume 8) these records detail a wide range of civic and legal activities including court proceedings, ordinances, elections, dispositions of property and correspondence. They provide precious insights into the lives, laws and customs of people living in 14th-century Aberdeen.  These books contain the earliest and most comprehensive archive of civic government records in Scotland and as such give historians the unique opportunity to trace and analyse patterns in the legal proceedings, governance, and social order of an urban city in the late Middle Ages.</p>
          <br>
          <img src="@/assets/images/aberdeenregisters1.jpg" alt="Registers Book Stack"/>
        </div>
      </div>
      <div class="column">
        <h2>Meet the Team</h2>
        <div class = "about-text">
          <br>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
          <br>
        </div>
      </div>
    </div>
  </div>

  <div>
    <Footer />
  </div>

</template>
