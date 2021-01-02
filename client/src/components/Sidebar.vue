<template>
  <v-navigation-drawer
    permanent
    mini-variant
    fixed
    class="mt-14 mt-md-16"
  >
    <v-list nav dense class="pt-2">
      <v-list-item link class="px-2" to="/minifigures">
        <v-list-item-icon>
          <v-icon>mdi-human-male</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Minifigures</v-list-item-title>
      </v-list-item>
      <v-list-item link to="/sets">
        <v-list-item-icon>
          <v-icon>mdi-toy-brick</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Sets</v-list-item-title>
      </v-list-item>
      <v-list-item link to="/statistics">
        <v-list-item-icon>
          <v-icon>mdi-chart-arc</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Statistics</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
