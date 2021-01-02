import {
  GET_MINIFIGURES,
  SET_MINIFIGURES,
  GET_MINIFIGURES_SUCCESS,
  GET_MINIFIGURES_ERROR,
  SET_MINIFIGURES_SUCCESS,
  SET_MINIFIGURES_ERROR,
} from '../types';

export default {
  [GET_MINIFIGURES](state, { data }) {
    state.minifigures = data;
  },
  [GET_MINIFIGURES_SUCCESS](state) {
    state.loading = false;
  },
  [GET_MINIFIGURES_ERROR](state, payload) {
    state.loading = false;
    state.error = payload;
  },

  [SET_MINIFIGURES](state, payload) {
    state.minifigures.push(payload);
  },
  [SET_MINIFIGURES_SUCCESS](state) {
    state.saving = false;
  },
  [SET_MINIFIGURES_ERROR](state, payload) {
    state.saving = false;
    state.error = payload;
  },
};
