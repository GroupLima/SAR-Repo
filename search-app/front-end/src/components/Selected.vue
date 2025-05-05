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
          <div class="record-field">
            <span class="record-label">Volume:</span>
            <span>{{ record.volume }}</span>
          </div>
          <div class="record-field">
            <span class="record-label">Page:</span>
            <span>{{ record.page }}</span>
          </div>
        </div>
        <div class="record-content">
          {{ record.content }}
        </div>
        <div class="record-content xml-content">
          <pre>{{ record.xml_content }}</pre>
        </div>
        <div class="record-actions">
          <button data-tooltip="Remove Item from Selected" class="remove-btn" @click="removeRecord(record.id)">Remove</button>
        </div>
      </div>
      
      <div class="actions">
        <button data-tooltip="Clear all Items from Selected" class="clear-btn" @click="clearAll">Clear All</button>
        <button data-tooltip="Download the Selected Items in PDF" class="export-pdf-btn" @click="exportToPDF">Export as PDF</button>
      </div>
    </div>
  </div>
</template>

<script>
import { inject } from 'vue';
import { PDFDocument, rgb } from 'pdf-lib';

export default {
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
    
    const exportToPDF = async () => {
      try {
        const pdfDoc = await PDFDocument.create();
        let currentPage = pdfDoc.addPage();
        const { width, height } = currentPage.getSize();
        const margin = 50;
        const lineHeight = 20;
        const fontSize = 12;
        let yPos = height - margin;
        
        // Add title
        currentPage.drawText('Selected Records', {
          x: margin,
          y: yPos,
          size: 18,
          color: rgb(0, 0, 0),
        });
        
        yPos -= 30;
    
        for (let i = 0; i < selectedRecords.value.length; i++) {
          const record = selectedRecords.value[i];
          
          // Check if we need a new page
          if (yPos < margin + 100) { // Give enough space for at least basic record info
            currentPage = pdfDoc.addPage();
            yPos = height - margin;
          }
    
          // Draw record header
          currentPage.drawText(`Record ${i + 1}:`, {
            x: margin,
            y: yPos,
            size: 14,
            color: rgb(0, 0, 0),
          });
          yPos -= lineHeight;
    
          // Add record metadata
          const fields = [
            { label: 'ID', value: record.id },
            { label: 'Date', value: record.date },
            { label: 'Language', value: record.language },
            { label: 'Volume', value: record.volume },
            { label: 'Page', value: record.page }
          ];
    
          for (const field of fields) {
            // Check remaining space
            if (yPos < margin + 20) {
              currentPage = pdfDoc.addPage();
              yPos = height - margin;
            }
            
            currentPage.drawText(`${field.label}: ${field.value || 'N/A'}`, {
              x: margin + 10,
              y: yPos,
              size: fontSize,
              color: rgb(0, 0, 0),
            });
            yPos -= lineHeight;
          }
    
          // Add content with word wrapping
          if (yPos < margin + 40) {
            currentPage = pdfDoc.addPage();
            yPos = height - margin;
          }
          
          currentPage.drawText('Content:', {
            x: margin + 10,
            y: yPos,
            size: fontSize,
            color: rgb(0, 0, 0),
          });
          yPos -= lineHeight;
    
          // Word wrapping for content
          if (record.content) {
            yPos = drawWrappedText(currentPage, record.content, margin + 20, yPos, width - margin * 2 - 20, fontSize, lineHeight, pdfDoc);
          }
          
          // Check for space before adding XML content
          if (yPos < margin + 40) {
            currentPage = pdfDoc.addPage();
            yPos = height - margin;
          }
    
          // XML Content
          currentPage.drawText('XML Content:', {
            x: margin + 10,
            y: yPos,
            size: fontSize,
            color: rgb(0, 0, 0),
          });
          yPos -= lineHeight;
    
          // Word wrapping for XML content
          if (record.xml_content) {
            yPos = drawWrappedText(currentPage, record.xml_content, margin + 20, yPos, width - margin * 2 - 20, fontSize, lineHeight, pdfDoc);
          }
    
          // Add a separator between records
          yPos -= lineHeight * 1.5;
          
          // Always ensure at least 50 pts of padding at the bottom
          if (yPos < margin + 50) {
            currentPage = pdfDoc.addPage();
            yPos = height - margin;
          }
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
    
    // Helper function to draw wrapped text
    function drawWrappedText(page, text, x, y, maxWidth, fontSize, lineHeight, pdfDoc) {
      const { height } = page.getSize();
      const margin = 50;
      const words = text.split(' ');
      let line = '';
      
      for (let i = 0; i < words.length; i++) {
        const testLine = line + words[i] + ' ';
        const testWidth = testLine.length * (fontSize * 0.5); // Approximation for width
        
        if (testWidth > maxWidth && i > 0) {
          // Check if we need a new page
          if (y < margin + 20) {
            page = pdfDoc.addPage();
            y = height - margin;
          }
          
          page.drawText(line, {
            x: x,
            y: y,
            size: fontSize,
            color: rgb(0, 0, 0),
          });
          
          line = words[i] + ' ';
          y -= lineHeight;
        } else {
          line = testLine;
        }
      }
      
      // Draw the last line
      if (line.trim().length > 0) {
        // Check if we need a new page
        if (y < margin + 20) {
          page = pdfDoc.addPage();
          y = height - margin;
        }
        
        page.drawText(line, {
          x: x,
          y: y,
          size: fontSize,
          color: rgb(0, 0, 0),
        });
        y -= lineHeight;
      }
      
      return y;
    }
    
    return {
      selectedRecords,
      removeRecord,
      clearAll,
      exportToPDF
    };
  }
}
</script>

