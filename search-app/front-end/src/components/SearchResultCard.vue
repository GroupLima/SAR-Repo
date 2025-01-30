<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    id: {
        type: Object,
        required: true
    },
    htmlContent: {
        type: Object,
        required: true
    }
})

</script>
<!-- view for one entry of the results -->
<template>
    <div>
        <h4>id {{ id }}</h4>
        <div v-html="htmlContent"></div> <!-- This will render the HTML content inside the div -->
        <br>
    
    </div>
</template>