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
    },
    htmlvolume: { 
        type: Object,
        required: true
    },
    htmlpage: {
        type: Object,
        required: true
    },
    htmldate: {
        type: Object,
        required: true
    }
})

</script>
<!-- view for one entry of the results -->
<template>
    <div>
        <h4>{{ id }}</h4>
        <div v-html="htmlContent"></div> <!-- This will render the HTML content inside the div -->
        <br>
        <div v-html="volumeHtml"></div>
        <div v-html="pageHtml"></div>
        <div v-html="dateHtml"></div>
    
    </div>
</template>