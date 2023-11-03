import axios from 'axios';

export default axios.create({
    baseURL: 'http://localhost:5000/v1.1',
    headers: {
        'Content-Type': 'application/json',
    },
});