<template>
  <v-app-bar
    app
    color="light"
    dark
  >
    <div class="d-flex align-center">
      <v-img
        alt="Vuetify Logo"
        class="shrink mr-2"
        contain
        src="../assets/Plastic_brick_red.svg"
        transition="scale-transition"
        width="40"
      />
    </div>
    <v-app-bar-title>Lego Database</v-app-bar-title>
    <v-spacer/>
    <template v-slot:extension>
      <v-tabs align-with-title>
        <v-tabs-slider color="yellow"></v-tabs-slider>
        <v-tab to="/minifigs">Minifigures</v-tab>
        <v-tab to="/sets">Sets</v-tab>
      </v-tabs>
    </template>
  </v-app-bar>
</template>
