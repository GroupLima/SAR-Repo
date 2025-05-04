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
          <button class="nav-btn" @click="goToFirstPage">&lt;&lt;</button>
          <button class="nav-btn" @click="goToPrevPage" :disabled="currentPage <= 1">&lt;</button>

          <div class="page-number-search">
            <span class="page-label">Page</span>
            <input type="number" v-model.number="currentPage" class="page-number-input" min="1" :max="volumes[currentVolume]" @keyup.enter="goToSpecificPage" />
            <span class="page-total">of {{ volumes[currentVolume] }}</span>
            <button class="page-go-btn" @click="goToSpecificPage">Go</button>
          </div>

          <button class="nav-btn" @click="goToNextPage" :disabled="currentPage >= volumes[currentVolume]">&gt;</button>
          <button class="nav-btn" @click="goToLastPage">&gt;&gt;</button>
        </div>

        <div class="records">
          <div v-for="record in records" :key="record.id" class="record-item">
            <div class="record-header">
              <div class="record-field"><span class="record-label">ID:</span><span>{{ record.id }}</span></div>
              <div class="record-field"><span class="record-label">Date:</span><span>{{ record.date }}</span></div>
              <div class="record-field"><span class="record-label">Language:</span><span>{{ record.language }}</span></div>
            </div>
            <div class="record-content">{{ record.content }}</div>
            <div class="record-actions">
              <button class="xml-btn" @click="viewXML(record.id)">XML</button>
              <div class="checkbox-container">
                <input type="checkbox" :id="`record-${record.id}-checkbox`" :checked="isRecordSelected(record.id)" @change="toggleRecordSelection(record)" />
                <label :for="`record-${record.id}-checkbox`">Add to selected</label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

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
import api from '@/services/api';

export default {
  data() {
    return {
      pageImage,
      currentVolume: 1,
      currentPage: 1,
      volumes: {},
      records: [],
      showXmlModal: false,
      currentXmlRecordId: '',
      currentXmlContent: '',
      zoomScale: 2.5,
      isZooming: false,
      transformOrigin: '0% 0%',
      isMobile: false,
      smallScreen: false,
      lastTapTime: 0,
      doubleTapDelay: 300,
      mouseX: 0,
      mouseY: 0,
    };
  },
  inject: ['selectedRecords'],
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
    this.checkDeviceSize();
    window.addEventListener('resize', this.checkDeviceSize);
    this.loadVolumes();
    this.loadRecords();
  },
  unmounted() {
    window.removeEventListener('resize', this.checkDeviceSize);
  },
  methods: {
    isRecordSelected(id) {
      return this.selectedRecords.value.some(r => r.id === id);
    },
    toggleRecordSelection(record) {
      const index = this.selectedRecords.value.findIndex(r => r.id === record.id);
      if (index === -1) this.selectedRecords.value.push({ ...record });
      else this.selectedRecords.value.splice(index, 1);
    },
    async loadVolumes() {
      try {
        const res = await api.get('/volumes');
        this.volumes = res.data;
      } catch (e) {
        console.error('Volumes error:', e);
      }
    },
    async loadRecords() {
      try {
        const res = await api.get('/records', {
          params: { volume: this.currentVolume, page: this.currentPage }
        });
        this.records = res.data.records;
      } catch (e) {
        console.error('Records error:', e);
      }
    },
    handleVolumeChange() {
      this.currentPage = 1;
      this.loadRecords();
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
      const max = this.volumes[this.currentVolume];
      if (this.currentPage < 1) this.currentPage = 1;
      else if (this.currentPage > max) this.currentPage = max;
      this.loadRecords();
    },
    async viewXML(recordId) {
      this.currentXmlRecordId = recordId;
      try {
        const res = await api.get(`/records/${recordId}/xml`);
        this.currentXmlContent = res.data.xml || 'No XML content found.';
      } catch (e) {
        console.error('XML error:', e);
        this.currentXmlContent = 'Error fetching XML content.';
      }
      this.showXmlModal = true;
    },
    closeXmlModal() {
      this.showXmlModal = false;
    },
    copyXmlContent() {
      navigator.clipboard.writeText(this.currentXmlContent)
        .then(() => alert('Copied!'))
        .catch(() => alert('Copy failed.'));
    },
    checkDeviceSize() {
      this.isMobile = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
      this.smallScreen = window.innerWidth <= 768;
    },
    handleZoom(e) {
      const rect = this.$refs.pageImageRef.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      this.transformOrigin = `${x}% ${y}%`;
      if (!this.smallScreen && !this.isMobile) this.isZooming = true;
    },
    toggleZoom(e) {
      const rect = this.$refs.pageImageRef.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      this.transformOrigin = `${x}% ${y}%`;
      this.isZooming = !this.isZooming;
    },
    handleTouchStart(e) {
      if (!this.$refs.pageImageRef) return;
      e.preventDefault();
      if (e.touches.length === 1) {
        const touch = e.touches[0];
        const rect = this.$refs.pageImageRef.getBoundingClientRect();
        const x = ((touch.clientX - rect.left) / rect.width) * 100;
        const y = ((touch.clientY - rect.top) / rect.height) * 100;
        this.transformOrigin = `${x}% ${y}%`;
        const now = new Date().getTime();
        if (now - this.lastTapTime < this.doubleTapDelay) this.isZooming = !this.isZooming;
        this.lastTapTime = now;
      }
    },
    handleTouchMove(e) {
      e.preventDefault();
      if (!this.isZooming) return;
      const touch = e.touches[0];
      const rect = this.$refs.pageImageRef.getBoundingClientRect();
      const x = ((touch.clientX - rect.left) / rect.width) * 100;
      const y = ((touch.clientY - rect.top) / rect.height) * 100;
      this.transformOrigin = `${x}% ${y}%`;
    },
    handleTouchEnd() {},
    resetZoom() {
      if (!this.smallScreen && !this.isMobile) this.isZooming = false;
    }
  }
};
</script>
