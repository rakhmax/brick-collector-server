<template>
  <v-data-table
    :headers="headers"
    :items="minifigures"
    :loading="$store.state.loading"
    :search="search"
    class="elevation-1"
    group-by="theme"
    loading-text="Loading minifigures..."
  >
    <template v-slot:item.theme="{ item }">
      <span>{{ $store.state.themes.find((theme) => {
        return theme.id === item.theme;
      }).name }}</span>
    </template>
    <template v-slot:top>
      <v-text-field
        v-model="search"
        label="Search"
        class="mx-4"
      />
    </template>
  </v-data-table>
</template>

<script>
import { GET_MINIFIGURES } from '@/store/types';

export default {
  name: 'TableMinifigures',

  data: () => ({
    search: '',
    headers: [
      // { text: 'ID', value: 'number' },
      {
        text: 'Name',
        align: 'start',
        value: 'name',
      },
      { text: 'Theme', value: 'theme' },
      { text: 'Price', value: 'price' },
      { text: 'Number of dups', value: 'duplicated' },
      {
        text: 'Comment',
        sortable: false,
        value: 'comment',
      },
    ],
    minifigures: [],
  }),

  methods: {
    async getAll() {
      await this.$store.dispatch(GET_MINIFIGURES);
      this.minifigures = this.$store.state.minifigures;
    },
  },

  async mounted() {
    this.getAll();
  },
};
</script>
