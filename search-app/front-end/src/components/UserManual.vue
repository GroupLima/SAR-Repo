<template>
    <div>
        <button class="UserManual" @click="showUserManual">User Manual</button>

    </div>
</template>


<script>
import router from '@/router';
export default {
    name: 'UserManual',
    methods: {
        showUserManual() {
            const routeUrl = this.$router.resolve({ name: 'usermanual' }).href;
            window.open(routeUrl, '_blank');
    
        }
    }
};

</script>

