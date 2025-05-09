<template>
  <div class="help-page">
    <!-- Content for the help page -->
    <h1>Help Page</h1>
    <p>This is the help page content.</p>
  </div>
</template>

<script>
export default {
    name: 'HelpPage',
    methods: {
        showHelpPage() {
            const routeUrl = this.$router.resolve({ name: 'help' }).href;
            window.open(routeUrl, '_blank');
        }
    }
};
</script>

<style scoped>
/* Add styles for the help page if needed */
.help-page {
  /* Example styles */
  padding: 20px;
}
</style>
