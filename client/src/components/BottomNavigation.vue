<template>
  <v-bottom-navigation
    v-model="value"
    grow
    fixed
  >
    <v-btn value="minifigures" to="/minifigures">
      <span>Minifigures</span>
      <v-icon>mdi-human-male</v-icon>
    </v-btn>
    <v-btn value="sets" to="/sets">
      <span>Sets</span>
      <v-icon>mdi-toy-brick</v-icon>
    </v-btn>
    <v-btn value="stats" to="/statistics">
      <span>Statistics</span>
      <v-icon>mdi-chart-arc</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>
