<script>
import router from '@/router';
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

<template>
    <div>
        <Footer />
    </div>
</template>