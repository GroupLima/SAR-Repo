<template>
  <div class="container-browser">
    <div class="volume-nav">
      <select data-tooltip="Select the Preferred Volume" class="volume-select" v-model="currentVolume" @change="handleVolumeChange">
        <option v-for="(pageCount, volId) in volumes" :key="volId" :value="Number(volId)">
          Volume {{ volId }}
        </option>
      </select>
    </div>
    
    <div class="split-view">
      <div class="image-viewer" ref="imageViewer">
        <img 
          :src="pageImage" 
          alt="Page Image" 
          class="page-image" 
          @mousemove="handleZoom" 
          @mouseleave="resetZoom"
          ref="pageImageRef"
          :style="imageStyle"
        />
      </div>
      
      <div class="records-container">
        <div class="page-navigation">
          <button data-tooltip="Click Here to go to the First Page of the Volume" class="nav-btn" @click="goToFirstPage">&lt;&lt;</button>
          <button data-tooltip="Click here for the previous Page" class="nav-btn" @click="goToPrevPage" :disabled="currentPage <= 1">&lt;</button>
          
          <!-- Updated page number search component -->
          <div class="page-number-search">
            <span class="page-label">Page</span>
            <input 
              type="number" 
              v-model.number="currentPage" 
              class="page-number-input" 
              min="1" 
              :max="volumes[currentVolume]"
              @keyup.enter="goToSpecificPage"
            />
            <span class="page-total">of {{ volumes[currentVolume] }}</span>
            <button class="page-go-btn" @click="goToSpecificPage" data-tooltip="Go to specified page">Go</button>
          </div>
          
          <button data-tooltip="Click Here for the Next Page" class="nav-btn" @click="goToNextPage" :disabled="currentPage >= volumes[currentVolume]">&gt;</button>
          <button data-tooltip="Click here to go the Last Page of the Volume" class="nav-btn" @click="goToLastPage">&gt;&gt;</button>
        </div>
        
        <div class="records">
          <div v-for="record in records" :key="record.id" class="record-item">
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
              <button data-tooltip="Click Here to See the XML Format of the Content" class="xml-btn" @click="viewXML(record.id)">XML</button>
              <div data-tooltip="Click Here to Add the Content to the Selected Page" class="checkbox-container">
                <input 
                  type="checkbox" 
                  :id="`record-${record.id}-checkbox`" 
                  :checked="isRecordSelected(record.id)"
                  @change="toggleRecordSelection(record)"
                >
                <label :for="`record-${record.id}-checkbox`">Add to selected</label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- XML Modal -->
    <div v-if="showXmlModal" class="xml-modal-overlay">
      <div class="xml-modal">
        <div class="xml-modal-header">
          <h3>XML Content: {{ currentXmlRecordId }}</h3>
          <button class="close-btn" @click="closeXmlModal">&times;</button>
        </div>
        <div class="xml-modal-body">
          <pre class="xml-content">{{ currentXmlContent }}</pre>
        </div>
        <div class="xml-modal-footer">
          <button class="copy-btn" @click="copyXmlContent">Copy to Clipboard</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import pageImage from '@/assets/images/try_one.jpeg';
import { inject, ref, computed } from 'vue';

export default {
  data() {
    return {
      pageImage,
      currentVolume: 1,
      currentPage: 1,
      volumes: {
        1: 20,
        2: 15,
        4: 25,
        5: 18,
        6: 22,
        7: 16,
        8: 19
      },
      records: [
        {
          id: 'ARO-1-0001-01',
          date: '1398-09-30',
          language: 'Latin',
          content: 'H Processus Curiarum Balliuorum Isti Sunt...'
        },
        {
          id: 'ARO-1-0001-02',
          date: '1398-09-30',
          language: 'Latin',
          content: 'Quo die Willelmus de Camera pater cum...'
        }
      ],
      // XML Modal properties
      showXmlModal: false,
      currentXmlRecordId: '',
      currentXmlContent: '',
      xmlData: {
        'ARO-1-0001-01': '<div type="heading" xml:id="ARO-1-0001-01" xml:lang="lat">\n  <head>Processus Curiarum Balliuorum Isti Sunt</head>\n  <p><lb break="yes"/>qui incipiunt die lune  proximo  post festum beati michaelis archangeli Anno<lb break="yes"/>Domini Millesimo  ccc<hi rend="superscript">mo</hi>  nonogesimo  Octauo .</p>\n</div>',
        'ARO-1-0001-02': '<div type="heading" xml:id="ARO-1-0001-02" xml:lang="lat">\n  <head>Quo die Willelmus de Camera pater</head>\n  <p><lb break="yes"/>cum pertinentiis quibuscumque...</p>\n</div>'
      },
      // Zoom properties
      zoomScale: 2, // Scale factor when zooming
      isZooming: false,
      zoomX: 0,
      zoomY: 0,
      transformOrigin: '0% 0%'
    }
  },
  setup() {
    // Inject the shared selectedRecords state
    const selectedRecords = inject('selectedRecords', ref([]));
    const pageImageRef = ref(null);
    const imageViewer = ref(null);
    
    // Check if a record is selected
    const isRecordSelected = (recordId) => {
      return selectedRecords.value.some(record => record.id === recordId);
    };
    
    // Toggle record selection
    const toggleRecordSelection = (record) => {
      const index = selectedRecords.value.findIndex(r => r.id === record.id);
      
      if (index === -1) {
        // Add to selected records if not already there
        selectedRecords.value.push({ ...record });
      } else {
        // Remove from selected records
        selectedRecords.value.splice(index, 1);
      }
    };
    
    return {
      selectedRecords,
      isRecordSelected,
      toggleRecordSelection,
      pageImageRef,
      imageViewer
    };
  },
  computed: {
    imageStyle() {
      if (!this.isZooming) {
        return {
          transform: 'scale(1)',
          transformOrigin: 'center center'
        };
      }
      
      return {
        transform: `scale(${this.zoomScale})`,
        transformOrigin: this.transformOrigin,
        transition: 'transform 0.1s ease-out'
      };
    }
  },
  mounted() {
    this.loadRecords();
  },
  methods: {
    handleVolumeChange() {
      this.currentPage = 1;
      this.loadRecords();
      console.log(`Changed to Volume ${this.currentVolume}, Page ${this.currentPage}`);
    },
    goToFirstPage() {
      this.currentPage = 1;
      this.loadRecords();
    },
    goToPrevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.loadRecords();
      }
    },
    goToNextPage() {
      if (this.currentPage < this.volumes[this.currentVolume]) {
        this.currentPage++;
        this.loadRecords();
      }
    },
    goToLastPage() {
      this.currentPage = this.volumes[this.currentVolume];
      this.loadRecords();
    },
    goToSpecificPage() {
      // Ensure the page is within valid range
      const maxPage = this.volumes[this.currentVolume];
      
      if (this.currentPage < 1) {
        this.currentPage = 1;
      } else if (this.currentPage > maxPage) {
        this.currentPage = maxPage;
      }
      
      this.loadRecords();
    },
    viewXML(recordId) {
      this.currentXmlRecordId = recordId;
      this.currentXmlContent = this.xmlData[recordId] || 'XML content not found';
      this.showXmlModal = true;
      console.log(`Viewing XML for record ${recordId}`);
    },
    closeXmlModal() {
      this.showXmlModal = false;
    },
    copyXmlContent() {
      navigator.clipboard.writeText(this.currentXmlContent)
        .then(() => {
          alert('XML content copied to clipboard!');
        })
        .catch(err => {
          console.error('Failed to copy: ', err);
          alert('Failed to copy XML content. Please try again.');
        });
    },
    loadRecords() {
      console.log(`Loading records for Volume ${this.currentVolume}, Page ${this.currentPage}`);
      // Here you would typically fetch records from an API
      // For now we'll just use the static records in data()
    },
    
    // Direct image zoom methods
    handleZoom(event) {
      if (!this.$refs.pageImageRef) return;
      
      const rect = this.$refs.pageImageRef.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      
      this.transformOrigin = `${x}% ${y}%`;
      this.isZooming = true;
    },
    
    resetZoom() {
      this.isZooming = false;
    }
  }
}
</script>