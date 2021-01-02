import axios from 'axios';
import http from '../../axios';
import { GET_DOLLAR_RATE, GET_THEMES } from '../types';

export default {
  async [GET_DOLLAR_RATE]({ commit }) {
    const { data } = await axios.get('https://www.cbr-xml-daily.ru/latest.js');
    commit(GET_DOLLAR_RATE, data.rates.USD);
  },
  async [GET_THEMES]({ commit }) {
    const { data } = await http.get('/themes');
    commit(GET_THEMES, data);
  },
};
