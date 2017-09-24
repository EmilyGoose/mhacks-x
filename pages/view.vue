<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-xs-center">
        <img src="/logo.svg" alt="ARTiculate" class="mb-5" />
      </div>
      <v-card>
        <v-card-title class="headline">Here's your layout</v-card-title>
        <canvas id="artwork" height="400" width="300"></canvas>
        <video controls v-for="token in tokens" v-if="token.intent && token.intent === 'add_gif'">
          <source :src="token.url" type="video/mp4" />
        </video>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn primary flat nuxt to="/">Back</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>


<script>
export default {
  data: () => ({
    positions: []
  }),
  mounted () {
    const ctx = document.getElementById('artwork').getContext('2d')
    for (const polygon of this.tokens) {
      var x = polygon.position[0] * 100 + 100
      var y = (1 - polygon.position[1]) * 75 + 75
      /*let x = 150
      let y = 100
      if (polygon.origin && polygon.origin.contains('screen')) {
        if (polygon.direction && polygon.direction.contains('top')) {
          x = 150
          y = 50
        } else if (polygon.direction && polygon.direction.contains('bottom')) {
          x = 150
          y = 150
        } else if (polygon.direction && polygon.direction.contains('top')) {
          x = 150
          y = 50
        } else if (polygon.direction && polygon.direction.contains('right')) {
          x = 250
          y = 50
        } else if (polygon.direction && (polygon.direction.contains('middle') || polygon.direction.contains('center')|| polygon.direction.contains('centre'))) {
          x = 150
          y = 50
        }
      } else if (polygon.origin) {
        for (let obj of this.positions) {
          if (polygon.origin.contains(obj.shape)) {
            if (polygon.direction && polygon.direction.contains('top') && polygon.direction.contains('above')) {
              x = obj.x - 70
              y = obj.y
            } else if (polygon.direction && polygon.direction.contains('bottom')) {
              x = 150
              y = 150
            } else if (polygon.direction && polygon.direction.contains('top')) {
              x = 150
              y = 50
            } else if (polygon.direction && polygon.direction.contains('right')) {
              x = 250
              y = 50
            } else if (polygon.direction && (polygon.direction.contains('middle') || polygon.direction.contains('center')|| polygon.direction.contains('centre'))) {
              x = 150
              y = 50
            }
          }
          break
        }
      }*/
      if (polygon.colour) {
        ctx.fillStyle = polygon.colour
      }
      if (polygon.intent === 'draw_shape') {
        function drawPolygon(n) {
          const r = 50
          ctx.beginPath()
          ctx.moveTo(x + r * Math.cos(0), y + r * Math.sin(0))
          for (let i = 1; i < n; i++) {
            ctx.lineTo(x + r * Math.cos(2 * Math.PI * i / n), y + r * Math.sin(2 * Math.PI * i / n))
          }
          ctx.closePath()
          ctx.fill()
        }
        if (polygon.shape === 'circle') {
          ctx.beginPath()
          ctx.ellipse(x, y, 50, 50, 0, 0, 2 * Math.PI)
          ctx.fill()
          ctx.closePath()
        } else if (polygon.shape === 'square') {
          ctx.beginPath()
          ctx.fillRect(x - 25, y - 25, 50, 50)
          ctx.fill()
          ctx.closePath()
        } else if (polygon.shape === 'rectangle' || polygon.shape === 'box') {
          ctx.beginPath()
          ctx.fillRect(x - 50, y - 25, 100, 50)
          ctx.fill()
          ctx.closePath()
        } else if (polygon.shape === 'triangle') {
          drawPolygon(3)
        } else if (polygon.shape === 'pentagon') {
          drawPolygon(5)
        } else if (polygon.shape === 'hexagon') {
          drawPolygon(6)
        } else if (polygon.shape === 'heptagon' || polygon.shape === 'septagon') {
          drawPolygon(7)
        } else if (polygon.shape === 'octagon') {
          drawPolygon(8)
        } else if (polygon.shape === 'nonagon') {
          drawPolygon(9)
        } else if (polygon.shape === 'decagon') {
          drawPolygon(10)
        }
      } else if (polygon.intent === 'add_text') {
        ctx.font = '24px serif';
        ctx.fillText(polygon.text, x, y);
      }
      /*this.positions.push({
        x,
        y,
        shape: polygon.shape
      })*/
    }
  },
  computed: {
    tokens: function () {
      return this.$store.state.tokens
    }
  }
}
</script>
