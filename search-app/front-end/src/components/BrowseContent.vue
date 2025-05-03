<template>
  <div class="notification-banner">
    <div class="notification-content">
      <div class="notification-icon">ℹ️</div>
      <div class="notification-text">
        <strong>Please Note:</strong> While the Browse page UI is fully functional, it currently displays a placeholder record only. The record fetching functionality is still a work in progress and will be implemented in a future update.
      </div>
    </div>
  </div>
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
          @touchstart="handleTouchStart"
          @touchmove="handleTouchMove"
          @touchend="handleTouchEnd"
          @mousemove="handleZoom" 
          @click="toggleZoom"
          @mouseleave="resetZoom"
          ref="pageImageRef"
          :style="imageStyle"
        />
        <div v-if="isMobile || smallScreen" class="mobile-zoom-indicator" :class="{ active: isZooming }">
          <span v-if="isZooming">Click or double click to exit zoom</span>
          <span v-else>Click or double click to zoom</span>
        </div>
      </div>
      
      <div class="records-container">
        <div class="page-navigation">
          <button data-tooltip="Click Here to go to the First Page of the Volume" class="nav-btn" @click="goToFirstPage">&lt;&lt;</button>
          <button data-tooltip="Click here for the previous Page" class="nav-btn" @click="goToPrevPage" :disabled="currentPage <= 1">&lt;</button>
          
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
import { inject, ref, computed, onMounted } from 'vue';

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
      records: [],
      
      // XML Modal properties
      showXmlModal: false,
      currentXmlRecordId: '',
      currentXmlContent: '',
      xmlData: {
        'ARO-1-0001-01': '<div type="heading" xml:id="ARO-1-0001-01" xml:lang="lat">\n  <head>Processus Curiarum Balliuorum Isti Sunt</head>\n  <p><lb break="yes"/>qui incipiunt die lune  proximo  post festum beati michaelis archangeli Anno<lb break="yes"/>Domini Millesimo  ccc<hi rend="superscript">mo</hi>  nonogesimo  Octauo .</p>\n</div>',
        'ARO-1-0001-02': '<div type="heading" xml:id="ARO-1-0001-02" xml:lang="lat">\n  <head>Quo die Willelmus de Camera pater</head>\n  <p><lb break="yes"/>cum pertinentiis quibuscumque...</p>\n</div>'
      },
      // Zoom properties
      zoomScale: 2.5, // Increased zoom scale for better visibility
      isZooming: false,
      zoomX: 0,
      zoomY: 0,
      transformOrigin: '0% 0%',
      // Device specific properties
      isMobile: false,
      smallScreen: false,
      lastTouchX: 0,
      lastTouchY: 0,
      lastTapTime: 0,
      doubleTapDelay: 300, // milliseconds
      // Track mouse position for consistent zooming
      mouseX: 0,
      mouseY: 0
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
  async mounted() {
    this.checkDeviceSize();
    window.addEventListener('resize', this.checkDeviceSize);

    await this.loadVolumes();
    await this.loadRecords();
  },
  unmounted() {
    window.removeEventListener('resize', this.checkDeviceSize);
  },
  methods: {
    checkDeviceSize() {
      this.isMobile = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
      this.smallScreen = window.innerWidth <= 768;
    },
    async loadVolumes() {
    try {
      const response = await axios.get('/api/volumes');
      this.volumes = response.data;
    } catch (error) {
      console.error('Failed to fetch volumes:', error);
    }
    },
    async loadRecords() {
    try {
      const response = await axios.get('/api/records', {
        params: {
          volume: this.currentVolume,
          page: this.currentPage
        }
      });
      this.records = response.data.records;
    } catch (error) {
      console.error('Failed to fetch records:', error);
    }
    },
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
    
    // Zoom methods that work for both touch and mouse
    handleZoom(event) {
      if (!this.$refs.pageImageRef) return;
      
      const rect = this.$refs.pageImageRef.getBoundingClientRect();
      
      // Store mouse position for use in toggleZoom
      this.mouseX = event.clientX;
      this.mouseY = event.clientY;
      
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      
      this.transformOrigin = `${x}% ${y}%`;
      
      // Only auto-zoom on mousemove if not in small screen mode
      if (!this.smallScreen && !this.isMobile) {
        this.isZooming = true;
      }
    },
    
    // Toggle zoom on click (for both small screens and mobile)
    toggleZoom(event) {
      if (!this.$refs.pageImageRef) return;
      
      // If we're in small screen mode, toggle zoom state
      if (this.smallScreen || this.isMobile) {
        if (this.isZooming) {
          // If already zooming, turn it off
          this.isZooming = false;
        } else {
          // If not zooming, use the current mouse position as focal point
          const rect = this.$refs.pageImageRef.getBoundingClientRect();
          const x = ((event.clientX - rect.left) / rect.width) * 100;
          const y = ((event.clientY - rect.top) / rect.height) * 100;
          
          this.transformOrigin = `${x}% ${y}%`;
          this.isZooming = true;
        }
      }
    },
    
    // Mobile touch methods
    handleTouchStart(event) {
      if (!this.$refs.pageImageRef) return;
      
      // Prevent default behavior to avoid page scrolling when zooming
      event.preventDefault();
      
      // Handle single touch (positioning)
      if (event.touches.length === 1) {
        const touch = event.touches[0];
        this.lastTouchX = touch.clientX;
        this.lastTouchY = touch.clientY;
        
        const rect = this.$refs.pageImageRef.getBoundingClientRect();
        const x = ((touch.clientX - rect.left) / rect.width) * 100;
        const y = ((touch.clientY - rect.top) / rect.height) * 100;
        
        this.transformOrigin = `${x}% ${y}%`;
        
        // Toggle zoom on single tap
        const now = new Date().getTime();
        const timeSince = now - this.lastTapTime;
        
        if (timeSince < this.doubleTapDelay && timeSince > 0) {
          // Double tap - toggle zoom
          this.isZooming = !this.isZooming;
        }
        
        this.lastTapTime = now;
      }
    },
    
    handleTouchMove(event) {
      if (!this.$refs.pageImageRef || !this.isZooming) return;
      
      // Prevent default to avoid page scrolling
      event.preventDefault();
      
      const touch = event.touches[0];
      this.lastTouchX = touch.clientX;
      this.lastTouchY = touch.clientY;
      
      const rect = this.$refs.pageImageRef.getBoundingClientRect();
      const x = ((touch.clientX - rect.left) / rect.width) * 100;
      const y = ((touch.clientY - rect.top) / rect.height) * 100;
      
      this.transformOrigin = `${x}% ${y}%`;
    },
    
    handleTouchEnd(event) {
      // For mobile, we don't automatically reset zoom on touch end
      // as the zoom toggle is handled in touch start
    },
    
    resetZoom() {
      // Only reset zoom on mouse leave if not in small screen mode
      if (!this.smallScreen && !this.isMobile) {
        this.isZooming = false;
      }
    }
  }
}
</script>