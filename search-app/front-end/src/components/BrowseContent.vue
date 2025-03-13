<script>
import pageImage from '@/assets/images/try_one.jpeg';
import { inject, computed } from 'vue';

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
      ]
    }
  },
  setup() {
    // Inject the shared selectedRecords state
    const selectedRecords = inject('selectedRecords');
    
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
      toggleRecordSelection
    };
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
    viewXML(recordId) {
      console.log(`Viewing XML for record ${recordId}`);
      // Here you would typically show XML content in a modal or new view
    },
    loadRecords() {
      console.log(`Loading records for Volume ${this.currentVolume}, Page ${this.currentPage}`);
      // Here you would typically fetch records from an API
      // For now we'll just use the static records in data()
    }
  }
}
</script>

<template>
  <div class="container-browser">
    <div class="volume-nav">
      <select class="volume-select" v-model="currentVolume" @change="handleVolumeChange">
        <option v-for="(pageCount, volId) in volumes" :key="volId" :value="Number(volId)">
          Volume {{ volId }}
        </option>
      </select>
    </div>
    
    <div class="split-view">
      <div class="image-viewer">
        <img :src="pageImage" alt="Page Image" class="page-image" />
      </div>
      
      <div class="records-container">
        <div class="page-navigation">
          <button class="nav-btn" @click="goToFirstPage">&lt;&lt;</button>
          <button class="nav-btn" @click="goToPrevPage" :disabled="currentPage <= 1">&lt;</button>
          <div class="page-number">Page {{ currentPage }}</div>
          <button class="nav-btn" @click="goToNextPage" :disabled="currentPage >= volumes[currentVolume]">&gt;</button>
          <button class="nav-btn" @click="goToLastPage">&gt;&gt;</button>
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
              <button class="xml-btn" @click="viewXML(record.id)">XML</button>
              <div class="checkbox-container">
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
  </div>
  
</template>