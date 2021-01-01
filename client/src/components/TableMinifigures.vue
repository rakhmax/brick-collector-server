<template>
  <v-data-table
    :headers="headers"
    :items="minifigures"
    :loading="$store.state.loading"
    class="elevation-1"
    loading-text="Loading minifigures..."
  ></v-data-table>
</template>

<script>
import { GET_MINIFIGURES } from '@/store/types';

export default {
  name: 'TableMinifigures',

  data: () => ({
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
      try {
        await this.$store.dispatch(GET_MINIFIGURES);
        this.minifigures = this.$store.state.minifigures;
      } catch (error) {
        console.log(error);
      } finally {
        this.loading = false;
      }
    },
  },

  async mounted() {
    this.getAll();
  },
};
</script>
