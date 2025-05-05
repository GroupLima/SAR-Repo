<script setup>
import { ref } from 'vue';

const props = defineProps({
    record: {
        id: {
            type: String,
            required: true
        },
        date: {
            type: String,
            required: false
        },
        lang: {
            type: String,
            required: false
        },
        content: {
            type: String,
            required: true
        },
        xml_content: {
            type: String,
            required: true
        }
    }
    
});

// Reactive variable to control the display content
const showXml = ref(false);

// Toggle the content when the button is clicked
const toggleContent = () => {
  showXml.value = !showXml.value;
};
</script>

<template>
    <div>
        <div class="record-header">
            <div>ID: {{ record.id }}</div>
            <div>Date: {{ record.date }}</div>
            <div>Language: {{ record.lang }}</div>
        </div>

        <!-- Display either content or xml_content based on showXml value -->
        <div class="record-content">
            <div v-if="showXml">
                
                <!-- PLEASE HELP STYLE THIS -->
                <pre class="records-container">{{ record.xml_content }}</pre> <!-- Wrap XML content in <pre> tag -->
            
            </div>
            <div v-else>{{ record.content }}</div>
        </div>

        <!-- Button to toggle content -->
        <button class="xml-btn" @click="toggleContent">
            {{ showXml ? 'Switch to Content' : 'Switch to XML' }}
        </button>
     </div>
</template>