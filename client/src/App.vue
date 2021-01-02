<template>
  <v-app v-resize="onResize">
    <sidebar v-if="!isMobile"/>
    <v-main :class="!isMobile && 'ml-14'">
      <app-bar />
      <router-view />
      <v-btn
        :style="{ bottom: isMobile ? '56px' : 0 }"
        @click="dialog = true"
        color="light"
        fixed
        right
        class="my-4"
        fab
      >
        <v-icon dark>mdi-plus</v-icon>
      </v-btn>
      <dialog-add-item :dialog.sync="dialog" />
    </v-main>
    <bottom-navigation v-if="isMobile"/>
  </v-app>
</template>

<script>
import AppBar from '@/components/AppBar.vue';
import BottomNavigation from '@/components/BottomNavigation.vue';
import DialogAddItem from '@/components/DialogAddItem.vue';
import Sidebar from '@/components/Sidebar.vue';
import { GET_THEMES } from '@/store/types';

export default {
  name: 'App',

  components: {
    AppBar,
    BottomNavigation,
    DialogAddItem,
    Sidebar,
  },

  data: () => ({
    dialog: false,
    windowSize: {
      x: 0,
      y: 0,
    },
  }),

  mounted() {
    this.$store.dispatch(GET_THEMES);
    this.$vuetify.theme.dark = this.$store.state.darkMode;
    this.onResize();
  },

  methods: {
    onResize() {
      this.windowSize = { x: window.innerWidth, y: window.innerHeight };
    },
  },

  computed: {
    isMobile() {
      return this.windowSize.x < 600;
    },
  },
};
</script>
