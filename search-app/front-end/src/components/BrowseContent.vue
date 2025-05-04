<template>
  <div class="browse-page">
    <main class="content">
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
          <select class="volume-select" v-model="currentVolume" @change="handleVolumeChange">
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
              @click="toggleZoom"
              @mouseleave="resetZoom"
              ref="pageImageRef"
              :style="imageStyle"
            />
          </div>

          <div class="records-container">
            <div class="page-navigation">
              <button class="nav-btn" @click="goToFirstPage">&lt;&lt;</button>
              <button class="nav-btn" @click="goToPrevPage" :disabled="currentPage <= 1">&lt;</button>

              <input type="number" v-model.number="currentPage" min="1" :max="volumes[currentVolume]" @keyup.enter="goToSpecificPage" />
              <span>of {{ volumes[currentVolume] }}</span>
              <button class="page-go-btn" @click="goToSpecificPage">Go</button>

              <button class="nav-btn" @click="goToNextPage" :disabled="currentPage >= volumes[currentVolume]">&gt;</button>
              <button class="nav-btn" @click="goToLastPage">&gt;&gt;</button>
            </div>

            <div class="records">
              <div v-for="record in records" :key="record.id" class="record-item">
                <div class="record-header">
                  <div>ID: {{ record.id }}</div>
                  <div>Date: {{ record.date }}</div>
                  <div>Language: {{ record.language }}</div>
                </div>
                <div class="record-content">{{ record.content }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import pageImage from '@/assets/images/try_one.jpeg';
import { inject } from 'vue';
import api from '@/services/api';

export default {
  inject: ['selectedRecords'],
  data() {
    return {
      pageImage,
      currentVolume: 1,
      currentPage: 1,
      volumes: {},
      records: [],
      zoomScale: 2.5,
      isZooming: false,
      transformOrigin: '0% 0%',
    };
  },
  computed: {
    imageStyle() {
      if (!this.isZooming) {
        return { transform: 'scale(1)' };
      }
      return {
        transform: `scale(${this.zoomScale})`,
        transformOrigin: this.transformOrigin,
      };
    },
  },
  async mounted() {
    await this.loadVolumes();     // ✅ Ensure volumes are available before fetching records
    this.loadRecords();           // ✅ Will now use correct currentVolume and currentPage
    console.log(this.selectedRecords); // Confirm injection
  },
  methods: {
    async loadVolumes() {
      try {
        const response = await api.get('/volumes');
        this.volumes = response.data;
      } catch (error) {
        console.error('Failed to fetch volumes:', error);
      }
    },
    async loadRecords() {
      try {
        const response = await api.get('/records', {
          params: {
            volume: this.currentVolume,
            page: this.currentPage,
          },
        });
        this.records = response.data.records;
      } catch (error) {
        console.error('Failed to fetch records:', error);
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
    handleZoom(event) {
      const rect = this.$refs.pageImageRef.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      this.transformOrigin = `${x}% ${y}%`;
      this.isZooming = true;
    },
    toggleZoom(event) {
      const rect = this.$refs.pageImageRef.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      this.transformOrigin = `${x}% ${y}%`;
      this.isZooming = !this.isZooming;
    },
    resetZoom() {
      this.isZooming = false;
    },
  },
};
</script>
