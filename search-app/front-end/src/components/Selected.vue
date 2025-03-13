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
  
  <script setup>
  import '@/assets/sass/app.scss';
  </script>
  
  <script>
  import { inject } from 'vue';
  import { PDFDocument, rgb } from 'pdf-lib';
  
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
  
      const exportToPDF = async () => {
        const pdfDoc = await PDFDocument.create();
        const page = pdfDoc.addPage();
        const { width, height } = page.getSize();
        let yPos = height - 40;
  
        page.drawText('Selected Records', {
          x: 50,
          y: yPos,
          size: 18,
          color: rgb(0, 0, 0),
        });
        yPos -= 30;
  
        selectedRecords.value.forEach((record, index) => {
          page.drawText(`Record ${index + 1}:`, {
            x: 50,
            y: yPos,
            size: 12,
            color: rgb(0, 0, 0),
          });
          yPos -= 20;
  
          page.drawText(`ID: ${record.id}`, {
            x: 60,
            y: yPos,
            size: 12,
            color: rgb(0, 0, 0),
          });
          yPos -= 20;
  
          page.drawText(`Date: ${record.date}`, {
            x: 60,
            y: yPos,
            size: 12,
            color: rgb(0, 0, 0),
          });
          yPos -= 20;
  
          page.drawText(`Language: ${record.language}`, {
            x: 60,
            y: yPos,
            size: 12,
            color: rgb(0, 0, 0),
          });
          yPos -= 20;
  
          page.drawText(`Content: ${record.content}`, {
            x: 60,
            y: yPos,
            size: 12,
            color: rgb(0, 0, 0),
          });
          yPos -= 30;
        });
  
        const pdfBytes = await pdfDoc.save();
        const blob = new Blob([pdfBytes], { type: 'application/pdf' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'selected-records.pdf';
        link.click();
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