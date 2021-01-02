import Vue from 'vue';
import Vuex from 'vuex';

import { minifiguresActions, toolsActions } from './actions';
import { minifiguresMutations, toolsMutations } from './mutations';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    error: null,
    loading: false,
    saving: false,
    minifigures: [],
    sets: [],
    darkMode: window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches,
    dollarRate: 0,
  },
  mutations: {
    ...minifiguresMutations,
    ...toolsMutations,
  },
  actions: {
    ...minifiguresActions,
    ...toolsActions,
  },
  modules: {
  },
});
