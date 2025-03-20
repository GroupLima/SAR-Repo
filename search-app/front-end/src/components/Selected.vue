<template>
  <div class="selected-container">
    <h1>Selected Records</h1>
    
    <div v-if="selectedRecords.length === 0" class="no-records">
      No records selected. Go to Browse to select records.
    </div>
    
    <div v-else class="selected-records">
      <div v-for="record in selectedRecords" :key="record.id" class="record-item-s">
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
          <button data-tooltip="Remove Item from Selected" class="remove-btn" @click="removeRecord(record.id)">Remove</button>
        </div>
      </div>
      
      <div class="actions">
        <button data-tooltip = "Clear all Item from Selected" class="clear-btn" @click="clearAll">Clear All</button>
        <!--<button class="export-btn" @click="exportRecords">Export as JSON</button> -->
        <button data-tooltip ="Download the Selected Items in PDF" class="export-pdf-btn" @click="exportToPDF">Export as PDF</button>
      </div>
    </div>
  </div>
  <div>
    <Footer />  
  </div>
</template>

<script>
import { inject } from 'vue';
import { PDFDocument, rgb } from 'pdf-lib';
import Footer from '@/components/Footer.vue';

export default {
  components: {
    Footer,
  },
  setup() {
    const selectedRecords = inject('selectedRecords');
    
    if (!selectedRecords) {
      console.error('selectedRecords not provided');
      return { selectedRecords: { value: [] } };
    }
    
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
      try {
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

        for (let i = 0; i < selectedRecords.value.length; i++) {
          const record = selectedRecords.value[i];
          
          // Check if we need a new page
          if (yPos < 100) {
            const newPage = pdfDoc.addPage();
            yPos = height - 40;
          }

          page.drawText(`Record ${i + 1}:`, {
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

          // Content might be too long, so truncate if needed
          const content = record.content.length > 80 ? 
            record.content.substring(0, 80) + '...' : 
            record.content;
            
          page.drawText(`Content: ${content}`, {
            x: 60,
            y: yPos,
            size: 12,
            color: rgb(0, 0, 0),
          });
          yPos -= 30;
        }

        const pdfBytes = await pdfDoc.save();
        const blob = new Blob([pdfBytes], { type: 'application/pdf' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'selected-records.pdf';
        link.click();
      } catch (error) {
        console.error('Error generating PDF:', error);
        alert('Failed to generate PDF. Please try again.');
      }
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