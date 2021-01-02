<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      max-width="600px"
      persistent
    >
      <v-card>
        <v-card-title>
          <span class="headline">{{ 'Add ' + title }}</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <search-box v-model="dialogData.select" :error="error"/>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-select
                  v-model="dialogData.theme"
                  :items="$store.state.themes"
                  item-text="name"
                  item-value="id"
                  label="Theme"
                  required
                ></v-select>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  v-model="dialogData.price"
                  label="Price"
                  required
                  type="number"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
              >
                <v-text-field
                  v-model="dialogData.comment"
                  label="Comment (optional)"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="handleClose"
          >
            Close
          </v-btn>
          <v-btn
            :disabled="disabledSave"
            color="blue darken-1"
            text
            @click="handleSave"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { SET_MINIFIGURES } from '@/store/types';
import SearchBox from './SearchBox.vue';
import { eventBus } from '../main';
import { selectTheme } from '../helpers/selectThemeHelper';

export default {
  components: {
    SearchBox,
  },
  data: () => ({
    title: 'item',
    dialogData: {
      select: null,
      price: null,
      comment: null,
      theme: null,
    },
  }),
  props: {
    dialog: { type: Boolean, default: false },
  },
  methods: {
    handleClose() {
      this.$emit('update:dialog', false);
    },

    async handleSave() {
      const {
        comment,
        price,
        select,
        theme,
      } = this.dialogData;

      if (select) {
        const data = {
          ...select,
          theme,
          price,
          comment,
        };

        await this.$store.dispatch(SET_MINIFIGURES, data);
        this.handleClose();
      } else {
        this.error = { message: 'Select an item' };
      }
    },
  },
  computed: {
    disabledSave() {
      return !(this.dialogData.select && this.dialogData.price) || this.$store.state.saving;
    },
  },
  created() {
    eventBus.$on('search', ({ search }) => {
      selectTheme.call(this, search);
    });
  },
};
</script>
