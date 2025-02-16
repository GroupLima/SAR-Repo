<script setup>
import router from '@/router';
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

// copy the html content of the search result
function copyHtmlContent() {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = props.htmlContent;
    const textContent = tempDiv.textContent || tempDiv.innerText || "";
    navigator.clipboard.writeText(textContent);
}

</script>
<!-- view for one entry of the results -->
<template>
    <div>
        <div v-html="htmlContent"></div>
        <br>
        <div class="result-footer">
            <p class="result-info">
                ID: {{ id }},
                Volume: {{ htmlvolume }}, 
                Page: {{ htmlpage }},
                Date: {{ htmldate }}
            </p>
            <div class="result-buttons">
                <button
                    @click="copyHtmlContent">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/></svg>
                </button>
                <button
                    @click="router.push({ name: 'browse' })">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h280v80H200v560h560v-280h80v280q0 33-23.5 56.5T760-120H200Zm188-212-56-56 372-372H560v-80h280v280h-80v-144L388-332Z"/></svg>
                </button>
            </div>
        </div>
    </div>
</template>