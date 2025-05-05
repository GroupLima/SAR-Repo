const browseCache = {
    // Cache for storing the loaded records
    _recordsCache: {},
  
    // Check if records for a specific volume are cached
    hasRecords(volume) {
      return this._recordsCache.hasOwnProperty(volume);
    },

    // Get records for a specific volume
    getRecords(volume) {
      return this._recordsCache[volume] || [];
    },

    // Store records for a specific volume
    setRecords(volume, records) {
      this._recordsCache[volume] = records;
    }
};
  
export default browseCache;
