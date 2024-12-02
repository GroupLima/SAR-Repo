import './bootstrap';
import { createApp } from 'vue';
import Xquery from './resources/vue/xquery.vue';
import SearchButton from './resources/vue/search-button.vue';
import BasicSearchFields from './resources/vue/basic-search-fields.vue';

const app = createApp({});
app.component('search-xquery', Xquery);//looks like <search-query></search-query>
app.component('search-button', SearchButton);
app.component('basic-input', BasicSearchFields);
app.mount('#app');
