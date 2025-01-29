import axios from 'axios'

const apiClient = axios.create({
    baseURL: '/back-end',
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    },
});

export default apiClient;