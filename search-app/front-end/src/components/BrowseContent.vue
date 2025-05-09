<script setup>
import { reactive, onMounted, ref, computed, watch } from 'vue';
import RecordList from '@/components/RecordList.vue';
import pageImage from '@/assets/images/try_one.jpeg';
import LoadingAnimation from '@/components/LoadingAnimation.vue';
import browseCache from '@/services/browseCache.js';
import axios from 'axios';

const volumes = [1, 2, 4, 5, 6, 7, 8];

const browseState = reactive({
  pageImage: null,
  currentVolume: 1,
  currentPageName: '',
  currentPageIndex: 1,
  zoomScale: 2.5,
  isZooming: false,
  transformOrigin: '0% 0%',
  pagesLoading: true,
  pages: []
})

function onChangeVolume(){
  browseState.currentPageIndex = 1;
  browseState.currentPageName = browseState.pages[0]?.page || '';
  // update browseState and load relevant records
  loadRecordsForSingleVolume(browseState.currentVolume);
}

const loadRecordsForSingleVolume = async (volume) => {
  browseState.pagesLoading = true;
  try {
    // fetch records from back end
    if (!browseCache.hasRecords(volume)){
      const response = await axios.get('/api/records', {params: {volume: volume}});
      // store list of pages containing lists of records
      browseState.pages = response.data.records;
      // store volumes in cache for quick access
      browseCache.setRecords(volume, response.data.records);
      
    // no need to fetch twice
    } else {
      // retrieve from cache
      browseState.pages = browseCache.getRecords(volume);
    }

    const foundIndex = browseState.pages.findIndex(p => p.page === browseState.currentPageName);
    if (foundIndex !== -1) {
      browseState.currentPageIndex = foundIndex + 1;
    } else if (browseState.pages.length > 0) {
      browseState.currentPageIndex = 1;
      browseState.currentPageName = browseState.pages[0].page;
    }

    displayPageImage();

  } catch (error) {
    console.error('Failed to fetch volumes:', error);
  }
  browseState.pagesLoading = false
}

const goToSpecificPage = () => {
  const input = browseState.currentPageName.trim();

  // Try exact match first
  const exactIndex = browseState.pages.findIndex(p => p.page === input);
  if (exactIndex !== -1) {
    browseState.currentPageIndex = exactIndex + 1;
    return;
  }

  const inputNum = parseInt(input);

  // If input is a number, try to match numerically with page.page
  if (!isNaN(inputNum)) {
    const pageNumbers = browseState.pages
      .map((p, idx) => ({
        ...p,
        numeric: parseInt(p.page),
        index: idx
      }))
      .filter(p => !isNaN(p.numeric))
      .sort((a, b) => a.numeric - b.numeric);

    const closest = pageNumbers.find(p => p.numeric >= inputNum);

    if (closest) {
      browseState.currentPageIndex = closest.index + 1;
      browseState.currentPageName = closest.page;
      return;
    }
  }

  // Fallback: alphabetical closest match
  const sortedPages = [...browseState.pages].sort((a, b) => a.page.localeCompare(b.page));
  const fallback = sortedPages.find(p => p.page.localeCompare(input) >= 0);
  if (fallback) {
    const fallbackIndex = browseState.pages.findIndex(p => p.page === fallback.page);
    browseState.currentPageIndex = fallbackIndex + 1;
    browseState.currentPageName = fallback.page;
  }
};

const goToFirstPage = () => {
  browseState.currentPageName = browseState.pages[0].page;
  browseState.currentPageIndex = 1;
}

const goToLastPage = () => {
  browseState.currentPageName = browseState.pages[browseState.pages.length - 1].page;
  browseState.currentPageIndex = browseState.pages.length;
}

const goToPrevPage = () => {
  if (browseState.currentPageIndex > 1) {
    browseState.currentPageIndex--;
    browseState.currentPageName = browseState.pages[browseState.currentPageIndex - 1].page;
  }
}

const goToNextPage = () => {
  if (browseState.currentPageIndex < browseState.pages.length) {
    browseState.currentPageIndex++;
    browseState.currentPageName = browseState.pages[browseState.currentPageIndex - 1].page;
  }
}

const currentRecords = computed(() => {
  return browseState.pages?.[browseState.currentPageIndex - 1]?.records || [];
});

const currentPageName = computed(() => {
  return browseState.pages?.[browseState.currentPageIndex - 1]?.page || "";
});

const getPageIndex = (pageName) => {
  return browseState.pages?.findIndex(p => p.page === pageName) ?? -1;
}

const getDocIdPageIndex = async(docId) => {
  const response = await axios.get('/api/rawEntry', {params: {docId: docId}});
  
  // load records from relevant volume if entry exists
  if (response.data.success) {
    const volume = parseInt(response.data.volume)
    browseState.currentVolume = volume;
    await loadRecordsForSingleVolume(volume);
    return await getPageIndex(response.data.page);
  }
  return -1;
}

// image stuff
const pageImageRef = ref(null);

function displayPageImage(){
  // display placeholder page for now
  browseState.pageImage = pageImage;

  // display corresponding image here ...
}

function handleZoom(event) {
  const rect = pageImageRef.value.getBoundingClientRect();
  const x = ((event.clientX - rect.left) / rect.width) * 100;
  const y = ((event.clientY - rect.top) / rect.height) * 100;
  browseState.transformOrigin = `${x}% ${y}%`;
  browseState.isZooming = true;
}
function toggleZoom(event) {
  const rect = pageImageRef.value.getBoundingClientRect();
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

watch(() => [browseState.currentVolume, browseState.currentPageName], ([newVolume, newPage]) => {
  const url = new URL(window.location.href);
  url.searchParams.set('volume', newVolume);
  url.searchParams.set('page', newPage);
  url.searchParams.delete('docId');
  url.searchParams.delete('docPage');
  window.history.pushState({}, '', url);

  // Save to sessionStorage
  sessionStorage.setItem('browseState', JSON.stringify({
    volume: newVolume,
    page: newPage
  }));
});

watch(() => browseState.currentPageName, (newName) => {
  // Only update if we have pages loaded and the name isn't empty
  if (browseState.pages.length > 0 && newName.trim()) {
    const foundIndex = browseState.pages.findIndex(p => p.page === newName);
    if (foundIndex !== -1) {
      browseState.currentPageIndex = foundIndex + 1;
    }
  }
}, { immediate: true });

const setBrowseStateValues = async () => {
  // parse the url
  const urlParams = new URLSearchParams(window.location.search);
  let vol = parseInt(urlParams.get('volume'));
  let docPage = urlParams.get('docPage');
  let docId = urlParams.get('docId');
  let page = urlParams.get('page');
  
 // browse by docId ex. query param is docId=ARO-2-0098A-01
  if (docId) {
    const pageIndex = await getDocIdPageIndex(docId);
    if (pageIndex !== -1) {
      browseState.currentPageIndex = pageIndex + 1;
      browseState.currentPageName = browseState.pages[pageIndex].page;
      return;
    }
  }

  // 2. From docPage
  if (!isNaN(vol) && volumes.includes(vol) && docPage) {
    browseState.currentVolume = vol;
    await loadRecordsForSingleVolume(vol);
    const pageIndex = getPageIndex(docPage);
    if (pageIndex !== -1) {
      browseState.currentPageIndex = pageIndex + 1;
      browseState.currentPageName = docPage;
      return;
    }
  }

  // 3. From URL volume + page
  if (!isNaN(vol) && typeof page === 'string') {
    browseState.currentVolume = vol;
    browseState.currentPageName = page;
    return;
  }

  // 4. From sessionStorage
  const saved = sessionStorage.getItem('browseState');
  if (saved) {
    const parsed = JSON.parse(saved);
    if (volumes.includes(parsed.volume)) {
      browseState.currentVolume = parsed.volume;
      browseState.currentPageName = parsed.page;
    }
  }
};


onMounted(async () => {
  await setBrowseStateValues();

  // Fallback to default volume if necessary
  if (!volumes.includes(browseState.currentVolume)) {
    alert(`Volume ${browseState.currentVolume} does not exist. Loading Volume 1.`);
    browseState.currentVolume = 1;
    browseState.currentPageName = '';
  }

  await loadRecordsForSingleVolume(browseState.currentVolume);

  // Ensure page index is set correctly if not already
  if (!browseState.currentPageIndex || !browseState.currentPageName) {
    browseState.currentPageIndex = 1;
    browseState.currentPageName = browseState.pages[0]?.page || '';
  }
});

</script>

<template>
  <div class="browse-page">
    <main class="content">

      <!-- notification that image is a placeholder -->
      <div class="notification-banner">
        <div class="notification-content">
          <div class="notification-icon">ℹ️</div>
          <div class="notification-text">
            <strong>Please Note:</strong> While the record data is accurate, the imaged displayed for each page is just a placeholder example document. 
          </div>
        </div>
      </div>

      <div class="container-browser">
        <div class="volume-nav">
          <select class="volume-select" v-model="browseState.currentVolume" @change="onChangeVolume" :disabled="browseState.pagesLoading">
            <option v-for="volId in volumes" :key="volId" :value="volId">
              Volume {{ volId }}
            </option>
          </select>
        </div>

        <div>Volume: {{ browseState.currentVolume }}<span v-if="currentPageName != ''">, Page: {{ currentPageName }}</span></div>
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
            <div v-if="!browseState.pagesLoading" class="page-navigation">
              <button class="nav-btn" @click="goToFirstPage">&lt;&lt;</button>
              <button class="nav-btn" @click="goToPrevPage" :disabled="browseState.currentPageIndex <= 1">&lt;</button>

              <input type="string" v-model="browseState.currentPageName" @keyup.enter="goToSpecificPage" style="width: 48px; padding: 2px 4px; font-size: 0.9rem; text-align: center;"/>
              <span>of {{ browseState.pages[browseState.pages.length - 1]?.page || browseState.pages.length }}</span>
              <!-- <button class="page-go-btn" @click="goToSpecificPage">Go</button> -->

              <button class="nav-btn" @click="goToNextPage" :disabled="browseState.currentPageIndex >= browseState.pages.length">&gt;</button>
              <button class="nav-btn" @click="goToLastPage">&gt;&gt;</button>
            </div>
             <!-- Display loading text if pages are loading -->
             <div v-if="browseState.pagesLoading">
                <LoadingAnimation :loadingText="'Loading records, please wait'"/>
            </div>

            <!-- Display records once loading is complete -->
            <RecordList v-if="!browseState.pagesLoading" :records="currentRecords"/>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>