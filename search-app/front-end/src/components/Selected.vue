<template>
    <div class="selected-container">
      <h1>Selected Records</h1>
      
      <div v-if="selectedRecords.length === 0" class="no-records">
        No records selected. Go to Browse to select records.
      </div>
      
      <div v-else class="selected-records">
        <div v-for="record in selectedRecords" :key="record.id" class="record-item">
          <div class="record-header">
            <div class="record-field">
              <span class="record-label">ID:</span>
              <span>{{ record.id }}</span>
            </div>
            <div class="record-field">
              <span class="record-label">Date:</span>
              <span>{{ record.date }}</span>
            </div>
            <div class="record-field">
              <span class="record-label">Language:</span>
              <span>{{ record.language }}</span>
            </div>
          </div>
          <div class="record-content">
            {{ record.content }}
          </div>
          <div class="record-actions">
            <button class="remove-btn" @click="removeRecord(record.id)">Remove</button>
          </div>
        </div>
        
        <div class="actions">
          <button class="clear-btn" @click="clearAll">Clear All</button>
          <button class="export-btn" @click="exportRecords">Export as JSON</button>
          <button class="export-pdf-btn" @click="exportToPDF">Export as PDF</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { inject } from 'vue';
  import jsPDF from 'jspdf';
  
  export default {
    setup() {
      const selectedRecords = inject('selectedRecords');
      
      const removeRecord = (recordId) => {
        const index = selectedRecords.value.findIndex(r => r.id === recordId);
        if (index !== -1) {
          selectedRecords.value.splice(index, 1);
        }
      };
      
      const clearAll = () => {
        selectedRecords.value = [];
      };
      
      const exportRecords = () => {
        // Export as JSON
        const dataStr = JSON.stringify(selectedRecords.value, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
        const exportFileDefaultName = 'selected-records.json';
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
      };
  
      const exportToPDF = () => {
        const doc = new jsPDF();
  
       
        let yPos = 20;
  
        
        doc.setFontSize(18);
        doc.text('Selected Records', 10, yPos);
        yPos += 10;
  
        // Loop through selected records and add them to the PDF
        selectedRecords.value.forEach((record, index) => {
          doc.setFontSize(12);
          doc.text(`Record ${index + 1}:`, 10, yPos);
          yPos += 10;
  
          doc.text(`ID: ${record.id}`, 15, yPos);
          yPos += 10;
  
          doc.text(`Date: ${record.date}`, 15, yPos);
          yPos += 10;
  
          doc.text(`Language: ${record.language}`, 15, yPos);
          yPos += 10;
  
          doc.text(`Content: ${record.content}`, 15, yPos);
          yPos += 15; // Add extra space between records
        });
  
        // Save the PDF
        doc.save('selected-records.pdf');
      };
      
      return {
        selectedRecords,
        removeRecord,
        clearAll,
        exportRecords,
        exportToPDF
      };
    }
  }
  </script>