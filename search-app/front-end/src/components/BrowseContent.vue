<script setup>
import { reactive, onMounted, ref, computed, watch } from 'vue';
import RecordList from '@/components/RecordList.vue';
import api from '@/services/api';
import pageImage from '@/assets/images/try_one.jpeg';
import LoadingAnimation from '@/components/LoadingAnimation.vue';
import browseCache from '@/services/browseCache.js';

const volumes = [1, 2, 4, 5, 6, 7, 8];

const browseState = reactive({
  pageImage: null,
  currentVolume: 1,
  currentPage: 1, // limited to the length of pages - 1
  currentPageName: '1',
  zoomScale: 2.5,
  isZooming: false,
  transformOrigin: '0% 0%',
  pagesLoading: true,
  pages: []
})

function onChangeVolume(){
  browseState.currentPage = 1;
  // update browseState and load relevant records
  loadRecordsForSingleVolume(browseState.currentVolume);
}

const loadRecordsForSingleVolume = async (volume) => {
  browseState.pagesLoading = true;
  try {
    // fetch records from back end
    if (!browseCache.hasRecords(volume)){
      const response = await api.get('/records', {params: {volume: volume}});
      // store list of pages containing lists of records
      browseState.pages = response.data.records;
      // store volumes in cache for quick access
      browseCache.setRecords(volume, response.data.records);
      
    // no need to fetch twice
    } else {
      // retrieve from cache
      browseState.pages = browseCache.getRecords(volume);
    }
    displayPageImage();

  } catch (error) {
    console.error('Failed to fetch volumes:', error);
  }
  browseState.pagesLoading = false
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

const currentPageName = computed(() => {
  return browseState.pages?.[browseState.currentPage - 1]?.page || "";
});

const getPageIndex = (pageName) => {
  return browseState.pages?.findIndex(p => p.page === pageName) ?? -1;
}

const getDocIdPageIndex = async(docId) => {
  const response = await api.get('/rawEntry', {params: {docId: docId}});
  
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

watch(() => [browseState.currentVolume, browseState.currentPage], ([newVolume, newPage]) => {
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


const setBrowseStateValues = async() => {
    // parse the url
    const urlParams = new URLSearchParams(window.location.search);
    let vol = parseInt(urlParams.get('volume'));
    let docPage = urlParams.get('docPage');
    let docId = urlParams.get('docId');

    // browse by docId ex. query param is docId=ARO-2-0098A-01
    if (docId){
      const pageIndex = await getDocIdPageIndex(docId);
      // if page exists, find the page index and then load the relevant records
      if (pageIndex != -1){
        browseState.currentPage = pageIndex+1;
        return;
      }
    }
    
    // browse by docPage ex. query param is docPage=98A
    if (!isNaN(vol) && volumes.includes(vol)&& docPage){
      await loadRecordsForSingleVolume(vol);
      const pageIndex = getPageIndex(docPage);
      if (pageIndex != -1){
        browseState.currentVolume = vol;
        browseState.currentPage = pageIndex+1;
        return;
      }
    }

    // browse normally with volume and page
    let page = parseInt(urlParams.get('page'));

    if (isNaN(vol) && !isNaN(page)) {vol=1; page=1}
    else if (!isNaN(vol) && isNaN(page)) page = 1;
    else if (isNaN(vol) && isNaN(page)) {
      // Fall back to sessionStorage
      const saved = sessionStorage.getItem('browseState');
      if (saved) {
        const parsed = JSON.parse(saved);
        vol = parsed.volume;
        page = parsed.page;
      }
    }
    if (!isNaN(vol)) browseState.currentVolume = vol;
    if (!isNaN(page)) browseState.currentPage = page;
};

onMounted(async () => {
  await setBrowseStateValues();
  
  // if volume or volume and page not specified, try loading first page of first volume.
  if (!volumes.includes(browseState.currentVolume) ){
    // try loading first volume
    alert(`volume ${browseState.currentVolume} does not exist`);
    browseState.currentVolume = 1;
    browseState.currentPage = 1;
    
  }
  // load according to url parameters
  loadRecordsForSingleVolume(browseState.currentVolume)
  
});
</script>

<template>
  <div class="browse-page">
    <main class="content">
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
              <button class="nav-btn" @click="goToPrevPage" :disabled="currentPage <= 1">&lt;</button>

              <input type="string" v-model="browseState.currentPage" min="1" :max="browseState.pages.length" @keyup.enter="goToSpecificPage" style="width: 40px; padding: 2px 4px; font-size: 0.9rem; text-align: center;"/>
              <span>of {{ browseState.pages.length }}</span>
              <!-- <button class="page-go-btn" @click="goToSpecificPage">Go</button> -->

              <button class="nav-btn" @click="goToNextPage" :disabled="browseState.currentPage >= browseState.pages.length">&gt;</button>
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