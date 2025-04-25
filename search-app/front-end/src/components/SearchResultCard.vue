<script setup>
import router from '@/router';
import { ref, onMounted } from 'vue';


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
    date: {
        type: Object,
        required: true
    },
    htmllang: {
        type: String,
        required: true
    }
})

// copy the html content of the search result
const isCopied = ref(false);
function copyHtmlContent() {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = props.htmlContent;
    const textContent = tempDiv.textContent || tempDiv.innerText || "";
    navigator.clipboard.writeText(textContent);
    isCopied.value = true;
    setTimeout(() => {isCopied.value = false;}, 2000);
}

// opens the content in the browse page
const openContentInBrowse = () => {
    const browseParams = {
        id: props.id
    };
    router.push({
        name: 'browse',
        query: browseParams
    });
}

// return date string and date certainty
const formatDate = () => {
    const certainty = props.date?.cert ?? null;
    const when = props.date?.when ?? null;
    let dateStr = "unknown";

    if (when){
        dateStr = when;
    } else{
        const from = props.date?.from ?? null;
        const to = props.date?.to ?? null;
        if (from && to){
            dateStr = `${from} - ${to}`;
        } else if (from){
            dateStr = from;
        } else if (to){
            dateStr = to;
        }
    }
    console.log(date, certainty);
    return {date: dateStr, certainty: certainty};
}
const date = ref("");
const certainty = ref("");

onMounted(() =>{
    const dateResult = formatDate();
    date.value = dateResult.date;
    certainty.value = dateResult.certainty;
});
</script>
<!-- view for one entry of the results -->
<template>
    <div>
        <div class="result-content" v-html="htmlContent"></div>
        <div class="result-footer">
            <p class="result-info">
                ID: {{ id }},&nbsp;
                Volume: {{ htmlvolume }},&nbsp;
                Page: {{ htmlpage }},&nbsp;
                Date: {{ date }} (Certainty: {{ certainty.charAt(0).toUpperCase() + certainty.slice(1) }}),&nbsp;
                Language: {{ htmllang }}
            </p>
            <div class="result-buttons">
                <button v-if="!isCopied"
                    @click="copyHtmlContent"
                    title = "Copy text">
                    <svg xmlns="http://www.w3.org/2000/svg" height="26px" viewBox="0 -960 960 960" width="26px" fill="#e8eaed"><path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/></svg>
                </button>
                <svg v-else xmlns="http://www.w3.org/2000/svg" height="26px" viewBox="0 -960 960 960" width="26px" fill="#e8eaed"><path d="m424-296 282-282-56-56-226 226-114-114-56 56 170 170Zm56 216q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>
                <button
                    @click="openContentInBrowse"
                    title = "Open in Browse">
                    <svg xmlns="http://www.w3.org/2000/svg" height="26px" viewBox="0 -960 960 960" width="26px" fill="#e8eaed"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h280v80H200v560h560v-280h80v280q0 33-23.5 56.5T760-120H200Zm188-212-56-56 372-372H560v-80h280v280h-80v-144L388-332Z"/></svg>
                </button>
            </div>
        </div>
    </div>
</template>