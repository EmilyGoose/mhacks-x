<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-xs-center">
        <img src="/logo.svg" alt="ARTiculate" class="mb-5" />
      </div>
      <v-card>
        <v-card-title class="headline">Here's your layout</v-card-title>
        <canvas id="artwork"></canvas>
        <v-card-text>
          {{ tokens }}
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data: () => ({
    directions: ''
  }),
  mounted () {
    const ctx = document.getElementById('artwork').getContext('2d')
    for (const polygon of this.tokens) {
      if (polygon.colour) {
        ctx.fillStyle = polygon.colour
      }
      if (polygon.shape === 'circle') {
        ctx.beginPath()
        ctx.ellipse(150, 100, 50, 50, 0, 0, 2 * Math.PI)
        ctx.fill()
        ctx.closePath()
      } else if (polygon.shape === 'square') {
        ctx.beginPath()
        ctx.fillRect(125, 75, 50, 50)
        ctx.fill()
        ctx.closePath()
      } else if (polygon.shape === 'rectangle') {
        ctx.beginPath()
        ctx.fillRect(100, 50, 100, 50)
        ctx.fill()
        ctx.closePath()
      }
      /*for (i = 0; i < n; i++) {
        printf("%f %f\n",r * Math.cos(2 * Math.PI * i / n), r * Math.sin(2 * Math.PI * i / n));
      }*/
    }
  },
  computed: {
    tokens: function () {
      return this.$store.state.tokens
    }
  }
}
</script>
