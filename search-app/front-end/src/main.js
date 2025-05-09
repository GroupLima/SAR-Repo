import './assets/sass/app.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

app.mount('#app')

// Signal that Vue has mounted to trigger CSS transition for FOUC prevention
document.getElementById('app')?.setAttribute('data-v-app-mounted', 'true');
