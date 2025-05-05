<script setup>
import { ref, onMounted, inject } from 'vue';


const selectedRecords = inject('selectedRecords');

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
        page: {
            type: String,
            required: false
        },
        vol: {
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

// Toggle record selection
const toggleRecordSelection = () => {
    const index = selectedRecords.value.findIndex(r => r.id === props.record.id);
    
    if (index === -1) {

    // Add to selected records if not already there
    selectedRecords.value.push({ 
        id: props.record.id,
        language: props.record.lang,
        date: props.record.date,
        page: props.record.page,
        volume: props.record.volume,
        content: props.record.content,
        xml_content: props.record.xml_content
    });
    } else {
    // Remove from selected records
    selectedRecords.value.splice(index, 1);
    }
};

// Check if a record is selected
const isRecordSelected = () => {
    return selectedRecords.value.some(r => r.id === props.record.id);
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
            <div v-if="showXml" class="xml-content">
                <pre>{{ record.xml_content }}</pre>
            </div>
            <div v-else>{{ record.content }}</div>
        </div>
        <!-- toggle between xml and content view -->
        <button class="xml-btn" @click="toggleContent">
            {{ showXml ? 'Switch to Content' : 'Switch to XML' }}
        </button>

        <div>
            <label data-tooltip="Save entry to export later as a PDF">Save</label>
            <input 
                type="checkbox" 
                :id="`record-${record.id}-checkbox`"
                :checked="isRecordSelected()"
                @change="toggleRecordSelection"
            >
        </div>
     </div>
</template>