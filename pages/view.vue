<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-xs-center">
        <img src="/v.png" alt="Vuetify.js" class="mb-5" />
      </div>
      <v-card>
        <v-card-title class="headline">Here's your layout</v-card-title>
        <v-card-text>
          {{ tokens }}
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import mapState from 'vuex'
export default {
  data: () => ({
    directions: ''
  }),
  computed: mapState('tokens')
}
</script>
