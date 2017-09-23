<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-xs-center">
        <img src="/v.png" alt="Vuetify.js" class="mb-5" />
      </div>
      <v-card>
        <v-card-title class="headline">Tell us what you want your layout to look like.</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="directions"
              name="directions"
              label="Write your directions here..."
              multi-line
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn primary flat nuxt @click.stop="send()">Continue</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios'
export default {
  data: () => ({
    directions: ''
  }),
  methods: {
    async send () {
      const tokens = await axios.get('http://localhost:5000/syntax', {
        params: {
          text: this.directions
        }
      })
      this.$store.commit('setTokens', tokens)
      this.$router.redirect('/view')
    }
  }
}
</script>
