<script setup>
import { reactive, onMounted, ref, computed } from 'vue'
import RecordList from '@/components/RecordList.vue'
import api from '@/services/api'
import pageImage from '@/assets/images/try_one.jpeg';

const volumes = [1, 2, 4, 5, 6, 7, 8];

const browseState = reactive({
  pageImage: null,
  currentVolume: 1,
  currentPage: 1, // limited to the length of pages - 1
  currentPageName: '1',
  zoomScale: 2.5,
  isZooming: false,
  transformOrigin: '0% 0%',
  pages: []
  /* pages:
    [
      0: {
        'page': 'page1',
        'records: [
          {
            'date': '1504-03-10'
            'language': 'latin'
            'content': 'orgubrwnvwornwreqvwj  ou prirht oa;w',
            'xml': '<p>orgubrwnvwornwreqvwj  ou prirht oa;w<p>'
          },
          {
            'date': '1489-03-11'
            'language': 'latin'
            'content': 'greioiwfm;vinfobightnprmwvpin',
            'xml': '<p>greioiwfm;vinfobightnprmwvpin<p>'
          },
        ]
      },
      1: {
        'page': 'page2',
        'records: [
          {
            'date': '1509-09-15'
            'language': 'multiple'
            'content': 'OGURBV UeBIUOHEV',
            'xml': '<p>OGURBV UeBIUOHEV<p>'
          },
          {
            'date': '1510-01-02'
            'language': 'middle scots'
            'content': 'urgi)*98YHubqiGJNRVV OUH',
            'xml': '<p>urgi)*98YHubqiGJNRVV OUH<p>'
          },
        ]
      },
        etc...
    ]
  */
})

function onChangeVolume(){
  // update browseState and load relevant records
  loadRecordsForSingleVolume();
}

function displayPageImage(){
  // display placeholder page for now
  browseState.pageImage = pageImage;

  // display corresponding image here ...
}

const loadRecordsForSingleVolume = async (volume) => {
  // fetch records from back end
  try {
    const response = await api.get('/records', {params: {volume: volume}});
    browseState.pages = response.data.records;
    displayPageImage()
    
  } catch (error) {
    console.error('Failed to fetch volumes:', error);
  }

}

const goToFirstPage = () => browseState.currentPage = 1;

const goToLastPage = () => browseState.currentPage = browseState.pages.length;

const goToPrevPage = () => { if (browseState.currentPage > 1) browseState.currentPage--; }

const goToNextPage = () => { if (browseState.currentPage < browseState.pages.length) { browseState.currentPage++; } }

const goToSpecificPage = () => {
  const max = browseState.pages.length;
  if (browseState.currentPage < 1) browseState.currentPage = 1;
  else if (browseState.currentPage > max) browseState.currentPage = max;
}

const currentRecords = computed(() => {
  return browseState.pages?.[browseState.currentPage - 1]?.records || [];
});

// image stuff
const pageImageRef = ref(null);

function handleZoom(event) {
  const rect = pageImageRef.getBoundingClientRect();
  const x = ((event.clientX - rect.left) / rect.width) * 100;
  const y = ((event.clientY - rect.top) / rect.height) * 100;
  browseState.transformOrigin = `${x}% ${y}%`;
  browseState.isZooming = true;
}
function toggleZoom(event) {
  const rect = pageImageRef.getBoundingClientRect();
  const x = ((event.clientX - rect.left) / rect.width) * 100;
  const y = ((event.clientY - rect.top) / rect.height) * 100;
  browseState.transformOrigin = `${x}% ${y}%`;
  browseState.isZooming = !browseState.isZooming;
}
function resetZoom() {
  browseState.isZooming = false;
}

const imageStyle = computed(() => {
  if (!browseState.isZooming) {
    return { transform: 'scale(1)' };
  }
  return {
    transform: `scale(${browseState.zoomScale})`,
    transformOrigin: browseState.transformOrigin,
  };
});


const setBrowseStateValues = () => {
    // parse the url
    const urlParams = new URLSearchParams(window.location.search);
    browseState.currentVolume = urlParams.get('volume') || browseState.currentVolume;
    browseState.currentPage = urlParams.get('page') || browseState.currentPage;
};

onMounted(() => {
  setBrowseStateValues();
  // if volume or volume and page not specified, try loading first page of first volume.
  if (!volumes.includes(browseState.currentVolume) ){
    // try loading first volume
    alert('volume does not exist')

  } else {
    // load according to url parameters
    loadRecordsForSingleVolume(browseState.currentVolume)
  }

  // placeholder image for now
  
})
</script>

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
          <select class="volume-select" v-model="browseState.currentVolume" @change="onChangeVolume">
            <option v-for="volId in volumes" :key="volId" :value="volId">
              Volume {{ volId }}
            </option>
          </select>
        </div>

        <div class="split-view">
          <div class="image-viewer" ref="imageViewer">
            <img
              :src="browseState.pageImage"
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

              <input type="string" v-model="browseState.currentPage" min="1" :max="browseState.pages.length" @keyup.enter="goToSpecificPage" />
              <span>of {{ browseState.pages.length }}</span>
              <button class="page-go-btn" @click="goToSpecificPage">Go</button>

              <button class="nav-btn" @click="goToNextPage" :disabled="browseState.currentPage >= browseState.pages.length">&gt;</button>
              <button class="nav-btn" @click="goToLastPage">&gt;&gt;</button>
            </div>
            <RecordList :records="currentRecords"/>

            <div class="records">
              <div v-for="record in currentRecords" :key="record.id" class="record-item">
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

<!-- <script>
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
</script> -->
