
import { createApp } from 'vue';
import Xquery from '/xquery.vue';
import SearchComponent from './search-component.vue';
import BasicSearchFields from './basic-search-fields.vue';
import AdvancedSearchFields from './advanced-search-fields.vue';

import axios from 'axios';
axios.defaults.baseURL = 'https://your-api-base-url.com';


const app = createApp({
    mounted() {
        console.log('Vue app mounted');
    },
    data() {
        return {
            isDropdownOpen: true, // State to manage dropdown visibility for advanced search
        };
    },
    methods: {
        toggleDropdown() {
            this.isDropdownOpen = !this.isDropdownOpen; // Toggle dropdown visibility
        },
    },
});

app.component('search-xquery', Xquery); // looks like <search-query></search-query>
app.component('search-component', SearchComponent);
app.component('basic-section', BasicSearchFields);
app.component('advanced-section', AdvancedSearchFields);

app.mount('#app');
