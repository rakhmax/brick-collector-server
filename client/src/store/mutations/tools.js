import { GET_DOLLAR_RATE, GET_THEMES } from '../types';

export default {
  [GET_DOLLAR_RATE](state, payload) {
    state.dollarRate = payload;
  },
  [GET_THEMES](state, payload) {
    state.themes = payload;
  },
};
