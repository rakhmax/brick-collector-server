import axios from 'axios';
import { apiRootUrl } from './const';

const http = axios.create({
  baseURL: apiRootUrl,
  headers: {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json',
  },
});

export default http;
