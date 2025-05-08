<script setup>
import { ref, onMounted, inject } from 'vue';
import vkbeautify from 'vkbeautify';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';

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
const copyXmlSuccess = ref(false);
const copyContentSuccess = ref(false);
const formattedXml = ref('');
const highlightedXml = ref('')

onMounted(() => {
  try {
    formattedXml.value = vkbeautify.xml(props.record.xml_content, 5);
    highlightedXml.value = hljs.highlight(formattedXml.value, {
      language: 'xml',
      ignoreIllegals: true
    }).value;
  } catch (error) {
    console.error('Error formatting XML:', error);
    formattedXml.value = props.record.xml_content;
    highlightedXml.value = props.record.xml_content;
  }
});

// Copy XML content to clipboard
const copyXmlToClipboard = () => {
  navigator.clipboard.writeText(formattedXml.value)
    .then(() => {
      copyXmlSuccess.value = true;
      setTimeout(() => {
        copyXmlSuccess.value = false;
      }, 2000);
    })
    .catch(err => {
      console.error('Failed to copy XML: ', err);
    });
};

// Copy regular content to clipboard
const copyContentToClipboard = () => {
  navigator.clipboard.writeText(props.record.content)
    .then(() => {
      copyContentSuccess.value = true;
      setTimeout(() => {
        copyContentSuccess.value = false;
      }, 2000);
    })
    .catch(err => {
      console.error('Failed to copy content: ', err);
    });
};

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

// Function to copy the currently displayed content
const copyCurrentContent = () => {
  if (showXml.value) {
    copyXmlToClipboard();
  } else {
    copyContentToClipboard();
  }
};
</script>

<template>
      <div class="record-header">
          <div>ID: {{ record.id }}</div>
          <div>Date: {{ record.date }}</div>
          <div>Language: {{ record.lang }}</div>
      </div>

      <!-- Display either content or xml_content based on showXml value -->
      <div class="record-content">
        <div v-if="showXml" class="xml-content">
          <pre v-html="highlightedXml"></pre>
          <!--<pre >{{ formattedXml }}</pre> -->
        </div>
        <div v-else class="text-content">
          <div>{{ record.content }}</div>
        </div>
      </div>
  
      <div class="record-actions">
      <div class="action-buttons">
        <button class="xml-btn" @click="toggleContent">
          {{ showXml ? 'Switch to Content' : 'Switch to XML' }}
    </button>

    <button 
      class="copy-btn"
      @click="copyCurrentContent"
      title="Copy current content"
    >
      <template v-if="!((showXml && copyXmlSuccess) || (!showXml && copyContentSuccess))">
        <svg xmlns="http://www.w3.org/2000/svg" height="26px" viewBox="0 -960 960 960" width="26px" fill="#e8eaed">
          <path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/>
        </svg>
      </template>
      <template v-else>
        <svg xmlns="http://www.w3.org/2000/svg" height="26px" viewBox="0 -960 960 960" width="26px" fill="#e8eaed">
          <path d="m424-296 282-282-56-56-226 226-114-114-56 56 170 170Zm56 216q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/>
        </svg>
      </template>
    </button>
  </div>

  <div class="checkbox-container">
    <label data-tooltip="Save entry to export later as a PDF">Add to selected</label>
    <input 
        type="checkbox" 
        :id="`record-${record.id}-checkbox`"
        :checked="isRecordSelected()"
        @change="toggleRecordSelection"
    >
  </div>
</div>
</template>