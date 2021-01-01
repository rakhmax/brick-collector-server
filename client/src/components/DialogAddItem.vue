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
import { add } from '../api/minifigures';

export default {
  components: {
    SearchBox,
  },
  data: () => ({
    error: null,
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
      const { comment, price, select } = this.dialogData;

      if (select) {
        const data = {
          ...select,
          price,
          comment,
        };

        try {
          this.error = null;
          await add(data);
          this.$store.dispatch(SET_MINIFIGURES, data);
          this.handleClose();
        } catch (e) {
          this.error = { message: e.message };
        }
      } else {
        this.error = { message: 'Select an item' };
      }
    },
  },
  mounted() {
    switch (this.$route.name) {
      case 'Minifigs':
        this.title = 'minifig';
        break;
      case 'Sets':
        this.title = 'set';
        break;
      default:
        break;
    }
  },
  computed: {
    titleByRoute: {
      get() {
        return this.title;
      },
      set() {
        this.title = window.location.pathname;
      },
    },

    disabledSave() {
      return !(this.dialogData.select && this.dialogData.price);
    },
  },
};
</script>
