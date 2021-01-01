<template>
  <v-app>
    <v-row>
      <v-col>
        <v-navigation-drawer permanent mini-variant>
          <v-list-item class="px-2">
            <v-list-item-avatar>
              <v-img
                src="https://randomuser.me/api/portraits/men/85.jpg"
              ></v-img>
            </v-list-item-avatar>
            <v-list-item-title>John Leider</v-list-item-title>
            <v-btn icon @click.stop="mini = !mini">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
          </v-list-item>
          <v-divider></v-divider>
          <v-list dense>
            <v-list-item v-for="item in items" :key="item.title" link>
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-col>
      <v-col>
        <v-main>
          <app-bar />
          <router-view />
          <v-btn
            :style="{ position: 'fixed', bottom: 0, right: 0 }"
            @click="dialog = true"
            class="ma-5"
            dark
            fab
          >
            <v-icon dark> mdi-plus </v-icon>
          </v-btn>
          <dialog-add-item :dialog.sync="dialog" />
        </v-main>
      </v-col>
    </v-row>
  </v-app>
</template>

<script>
import AppBar from '@/components/AppBar.vue';
import DialogAddItem from '@/components/DialogAddItem.vue';

export default {
  name: 'App',

  components: {
    AppBar,
    DialogAddItem,
  },

  data: () => ({
    dialog: false,
  }),
};
</script>
