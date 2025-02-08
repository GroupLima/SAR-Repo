<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    id: {
        type: String,
        required: true
    },
    htmlContent: {
        type: String,
        required: true
    },
    htmlvolume: { 
        type: String,
        required: true
    },
    htmlpage: {
        type: String,
        required: true
    },
    htmldate: {
        type: String,
        required: true
    }
})

</script>
<!-- view for one entry of the results -->
<template>
    <div>
        <div v-html="htmlContent"></div>
        <br>
        <p>ID: {{ id }},
        Volume: {{ htmlvolume }}, 
        Page: {{ htmlpage }},
        Date: {{ htmldate }}</p>
    </div>
</template>