import Vue from 'vue';
import Vuex from 'vuex';
import { getMinifigures } from '../api/minifigures';
import {
  GET_MINIFIGURES,
  SET_MINIFIGURES,
  GET_SETS,
  SET_SETS,
  GET_MINIFIGURES_SUCCESS,
  GET_MINIFIGURES_ERROR,
} from './types';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    error: null,
    loading: false,
    minifigures: [],
    sets: [],
  },
  mutations: {
    [GET_MINIFIGURES](state, { data }) {
      state.minifigures = JSON.parse(data);
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
    [GET_SETS]() {},
    [SET_SETS]() {},
  },
  actions: {
    async [GET_MINIFIGURES]({ commit, state }) {
      try {
        state.loading = true;
        commit(GET_MINIFIGURES, await getMinifigures());
        commit(GET_MINIFIGURES_SUCCESS);
      } catch (error) {
        commit(GET_MINIFIGURES_ERROR, error);
      }
    },
    [SET_MINIFIGURES]({ commit }, payload) {
      commit(SET_MINIFIGURES, payload);
    },
  },
  modules: {
  },
});
