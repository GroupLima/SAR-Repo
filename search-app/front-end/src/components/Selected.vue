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
        <br>
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
import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import vkbeautify from 'vkbeautify';

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
        // Create a new PDF document
        const pdfDoc = await PDFDocument.create();
        
        // Embed the standard font
        const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
        const boldFont = await pdfDoc.embedFont(StandardFonts.HelveticaBold);
        
        // Add the first page
        let currentPage = pdfDoc.addPage();
        const { width, height } = currentPage.getSize();
        
        // Define layout parameters
        const margin = 50;
        const lineHeight = 14;
        const normalFontSize = 10;
        const headerFontSize = 16;
        const subheaderFontSize = 12;
        let yPos = height - margin;
        
        // Add title
        currentPage.drawText('Selected Records', {
          x: margin,
          y: yPos,
          size: headerFontSize + 2,
          font: boldFont,
          color: rgb(0, 0, 0),
        });
        
        yPos -= lineHeight * 2;

        // Process each record
        for (let i = 0; i < selectedRecords.value.length; i++) {
          const record = selectedRecords.value[i];
          
          // Always start a record on a new page if less than 150pt available
          if (yPos < height - margin - 150) {
            currentPage = pdfDoc.addPage();
            yPos = height - margin;
          }

          // Draw record header with proper spacing
          currentPage.drawText(`Record ${i + 1}:`, {
            x: margin,
            y: yPos,
            size: subheaderFontSize,
            font: boldFont,
            color: rgb(0, 0, 0),
          });
          yPos -= lineHeight * 1.5;

          // Add record metadata with consistent spacing
          const fields = [
            { label: 'ID', value: record.id },
            { label: 'Date', value: record.date },
            { label: 'Language', value: record.language },
            { label: 'Volume', value: record.volume },
            { label: 'Page', value: record.page }
          ];

          for (const field of fields) {
            // Check if we need a new page
            if (yPos < margin + lineHeight) {
              currentPage = pdfDoc.addPage();
              yPos = height - margin;
            }
            
            // Draw field label in bold
            currentPage.drawText(`${field.label}:`, {
              x: margin,
              y: yPos,
              size: normalFontSize,
              font: boldFont,
              color: rgb(0, 0, 0),
            });
            
            // Draw field value
            currentPage.drawText(`${field.value || 'N/A'}`, {
              x: margin + 60, // Fixed position for alignment
              y: yPos,
              size: normalFontSize,
              font: font,
              color: rgb(0, 0, 0),
            });
            
            yPos -= lineHeight;
          }
          
          // Add extra spacing after metadata
          yPos -= lineHeight / 2;

          // Content Section
          if (yPos < margin + 100) { // Ensure enough space for section header + some content
            currentPage = pdfDoc.addPage();
            yPos = height - margin;
          }
          
          currentPage.drawText('Content:', {
            x: margin,
            y: yPos,
            size: normalFontSize,
            font: boldFont,
            color: rgb(0, 0, 0),
          });
          yPos -= lineHeight;

          // Draw content with proper wrapping
          if (record.content) {
            const contentLines = splitTextIntoLines(record.content, font, normalFontSize, width - (margin * 2) - 20);
            
            for (const line of contentLines) {
              if (yPos < margin + lineHeight) {
                currentPage = pdfDoc.addPage();
                yPos = height - margin;
              }
              
              currentPage.drawText(line, {
                x: margin + 10,
                y: yPos,
                size: normalFontSize,
                font: font,
                color: rgb(0, 0, 0),
              });
              
              yPos -= lineHeight;
            }
          }
          
          // Add space after content
          yPos -= lineHeight;

          // XML Content Section
          if (yPos < margin + 100) { // Ensure enough space for XML section
            currentPage = pdfDoc.addPage();
            yPos = height - margin;
          }
          
          currentPage.drawText('XML Content:', {
            x: margin,
            y: yPos,
            size: normalFontSize,
            font: boldFont,
            color: rgb(0, 0, 0),
          });
          yPos -= lineHeight;

          // Format and draw XML content with proper wrapping
          if (record.xml_content) {
            // Use a smaller font for XML to better display structure
            const xmlFontSize = normalFontSize - 1;
            
            // Format XML using vkbeautify for proper indentation
            let formattedXml = vkbeautify.xml(record.xml_content, 2); // 2 spaces indentation
            const xmlLines = splitTextIntoLines(formattedXml, font, xmlFontSize, width - (margin * 2) - 20);
            
            for (const line of xmlLines) {
              if (yPos < margin + lineHeight) {
                currentPage = pdfDoc.addPage();
                yPos = height - margin;
              }
              
              // Calculate indentation based on XML nesting level (simplified)
              const indentLevel = (line.match(/^\s*/) || [''])[0].length / 2;
              const indentAmount = indentLevel * 10; // 10 points per indent level
              
              currentPage.drawText(line.trim(), {
                x: margin + 10 + indentAmount,
                y: yPos,
                size: xmlFontSize,
                font: font,
                color: rgb(0, 0, 0),
              });
              
              yPos -= lineHeight;
            }
          }
          
          // Add extra space between records
          yPos -= lineHeight * 2;
        }

        // Save and download the PDF
        const pdfBytes = await pdfDoc.save();
        const blob = new Blob([pdfBytes], { type: 'application/pdf' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'selected-records.pdf';
        link.click();
        
      } catch (error) {
        console.error('Error generating PDF:', error);
        alert('Failed to generate PDF: ' + (error.message || 'Unknown error'));
      }
    };
    
    /**
     * Splits text into lines that fit within the specified width
     * @param {string} text - The text to split
     * @param {Font} font - The pdf-lib font object
     * @param {number} fontSize - The font size
     * @param {number} maxWidth - The maximum width in points
     * @returns {string[]} An array of lines
     */
    function splitTextIntoLines(text, font, fontSize, maxWidth) {
      const lines = [];
      const paragraphs = text.split('\n');
      
      for (const paragraph of paragraphs) {
        if (paragraph.trim() === '') {
          lines.push('');
          continue;
        }
        
        const words = paragraph.split(' ');
        let currentLine = '';
        
        for (const word of words) {
          // Test if adding this word would exceed the max width
          const testLine = currentLine ? currentLine + ' ' + word : word;
          const testWidth = font.widthOfTextAtSize(testLine, fontSize);
          
          if (testWidth > maxWidth && currentLine !== '') {
            lines.push(currentLine);
            currentLine = word;
          } else {
            currentLine = testLine;
          }
        }
        
        if (currentLine) {
          lines.push(currentLine);
        }
      }
      
      return lines;
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

