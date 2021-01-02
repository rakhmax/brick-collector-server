<template>
  <v-autocomplete
    :error="!!error"
    :error-messages="error && error.message"
    :items="items"
    :loading="loading"
    :search-input.sync="search"
    :value="value"
    @input="$emit('input', $event)"
    autofocus
    clearable
    flat
    hide-no-data
    item-text="name"
    label="Search..."
    no-filter
    return-object
    required
  >
    <template v-slot:item="{ item }">
      <v-avatar class="mr-3 my-2" color="indigo">
        <img
          v-if="item.img"
          :alt="item.name"
          :src="item.img"
        >
        <span v-else>{{ item.name.charAt(0) }}</span>
      </v-avatar>
      <v-list-item-content>
        <v-list-item-title v-text="item.name"></v-list-item-title>
      </v-list-item-content>
    </template>
  </v-autocomplete>
</template>

<script>
import { debounce } from 'lodash';
import searchData from '../api/search';
import { eventBus } from '../main';

export default {
  name: 'App',

  props: ['value', 'error'],

  data: () => ({
    loading: false,
    items: [],
    search: null,
  }),
  watch: {
    search(val) {
      eventBus.$emit('search', {
        search: this.search,
      });
      if (val) {
        this.querySelections(val);
      } else {
        this.items = [];
      }
    },
  },
  methods: {
    querySelections: debounce(async function querySelectionsDebounced(v) {
      this.loading = true;

      try {
        const data = await searchData(v, this.$route.name.toLowerCase());

        this.items = data.map((item) => ({
          name: item.name,
          img: item.img,
          number: item.id,
        }));
      } catch (e) {
        console.log(e);
      } finally {
        this.loading = false;
      }
    }, 200),
  },
};
</script>
