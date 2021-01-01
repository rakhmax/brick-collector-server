<template>
  <div>
    <table-minifigures/>
  </div>
</template>

<script>
import TableMinifigures from '@/components/TableMinifigures.vue';

export default {
  name: 'Minifigs',

  components: {
    TableMinifigures,
  },

  data: () => ({
    dialog: false,
  }),
};
</script>
