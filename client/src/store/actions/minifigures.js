import { addMinifigure, getMinifigures } from '../../api/minifigures';
import {
  GET_MINIFIGURES,
  GET_MINIFIGURES_SUCCESS,
  GET_MINIFIGURES_ERROR,
  SET_MINIFIGURES,
  SET_MINIFIGURES_SUCCESS,
  SET_MINIFIGURES_ERROR,
} from '../types';

export default {
  async [GET_MINIFIGURES]({ commit, state }) {
    try {
      if (!state.minifigures.length) {
        state.loading = true;
        commit(GET_MINIFIGURES, await getMinifigures());
        commit(GET_MINIFIGURES_SUCCESS);
      }
    } catch (error) {
      commit(GET_MINIFIGURES_ERROR, error);
    }
  },

  async [SET_MINIFIGURES]({ commit, state }, payload) {
    try {
      state.saving = true;
      const { data } = await addMinifigure(payload);
      commit(SET_MINIFIGURES, data);
      commit(SET_MINIFIGURES_SUCCESS);
    } catch (error) {
      commit(SET_MINIFIGURES_ERROR, error);
    }
  },
};
