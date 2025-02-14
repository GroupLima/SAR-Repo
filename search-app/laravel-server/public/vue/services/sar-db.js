import axios from 'axios';

const sarApiClient = axios.create({
    baseURL: '/sar-db', // Set base URL
    timeout: 5000, // Optional: Set a timeout
});

export default sarApiClient;
