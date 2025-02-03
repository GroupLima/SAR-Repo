import axios from 'axios'

const apiClient = axios.create({
    baseURL: '/laravel-server',
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    },
});

export default apiClient;