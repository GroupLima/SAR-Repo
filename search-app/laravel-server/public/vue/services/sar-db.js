import axios from 'axios';

const sarApiClient = axios.create({
    baseURL: 'http://localhost:8000/api', // Set base URL
    timeout: 5000, // Optional: Set a timeout
});

export default sarApiClient;
