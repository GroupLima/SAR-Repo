<script>
import router from '@/router';


export default {
  data() {
    return {
      searchQuery: '',
      activeVolume: null,
      showPages: false,
      currentVolume: null,
      currentPage: null,
      volumes: [
        { id: 1, pages: Array.from({ length: 20 }, (_, i) => i + 1) },
        { id: 2, pages: Array.from({ length: 15 }, (_, i) => i + 1) },
        { id: 4, pages: Array.from({ length: 25 }, (_, i) => i + 1) },
        { id: 5, pages: Array.from({ length: 18 }, (_, i) => i + 1) },
        { id: 6, pages: Array.from({ length: 22 }, (_, i) => i + 1) },
        { id: 7, pages: Array.from({ length: 16 }, (_, i) => i + 1) },
        { id: 8, pages: Array.from({ length: 19 }, (_, i) => i + 1) },
      ],
      records: [
        {
          id: 'ARO-1-0001-01',
          date: '1398-09-30',
          language: 'Latin',
          content: 'H Processus Curiarum Balliuorum Isti Sunt...',
          selected: false
        },
        {
          id: 'ARO-1-0001-02',
          date: '1398-09-30',
          language: 'Latin',
          content: 'Quo die Willelmus de Camera pater cum...',
          selected: false
        }
      ]
    }
  },
  methods: {
    toggleVolume(volumeId) {
      if (this.activeVolume === volumeId) {
        this.showPages = !this.showPages
      } else {
        this.activeVolume = volumeId
        this.showPages = true
      }
    },
    selectPage(volumeId, page) {
      this.currentVolume = volumeId
      this.currentPage = page
      // Here you would typically fetch the records for this page
    }
  }
}
</script>
  
  
  <template>
    <div class="container-browser">
      <!-- Header -->
      <div class="header">
        <div class="header-left">
          <h1>Search Aberdeen Registers</h1>
          <input
            type="text"
            placeholder="Search for..."
            v-model="searchQuery"
          />
          <button class="search-btn">
            Search
          </button>
        </div>
      </div>
  
      <!-- Main Content -->
      <div class="main-content">
        <!-- Volume Navigation -->
        <div class="volume-nav">
          <div v-for="volume in volumes" :key="volume.id" class="volume-item">
            <button
              @click="toggleVolume(volume.id)"
              :class="{ 'active': volume.id === activeVolume }"
            >
              Volume {{ volume.id }}
            </button>
            <!-- Pages list -->
            <div v-if="volume.id === activeVolume && showPages" class="pages-list">
              <button
                v-for="page in volume.pages"
                :key="page"
                @click="selectPage(volume.id, page)"
                :class="{ 'active': currentPage === page }"
              >
                Page {{ page }}
              </button>
            </div>
          </div>
        </div>
  
        <!-- Content Area -->
        <div class="content-area">
          <div v-if="currentVolume && currentPage" class="current-page-info">
            <h2>Volume: {{ currentVolume }} Page: {{ currentPage }}</h2>
          </div>
  
          <!-- Records -->
          <div class="records">
            <div v-for="record in records" :key="record.id" class="record-item">
              <div class="record-header">
                <span>ID: {{ record.id }}</span>
                <span>Date: {{ record.date }}</span>
                <span>Language: {{ record.language }}</span>
              </div>
              <div class="record-content" v-html="record.content"></div>
              <div class="record-actions">
                <button class="xml-btn">
                  XML
                </button>
                <label class="select-record">
                  <input type="checkbox" v-model="record.selected" />
                  Add to selected
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  </template>
  
  