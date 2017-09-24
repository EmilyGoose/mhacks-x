<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-xs-center">
        <img src="/logo.svg" alt="ARTiculate" class="mb-5" />
      </div>
      <v-card>
        <v-card-title class="headline">Tell us what you want your layout to look like.</v-card-title>
        <v-card-text>
          {{ error }}
          <v-form>
            <v-text-field
              v-model="directions"
              name="directions"
              label="Write your directions here..."
              multi-line>
            </v-text-field>
            <v-btn fab dark small class="pink" @click.stop = "startListen()" >
              <v-icon dark>mic</v-icon>
            </v-btn>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn primary flat nuxt @click.stop="send()" :loading="loading">Continue</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios'
var recognition
export default {
  data: () => ({
    directions: '',
    error: '',
    loading: false
  }),
  methods: {

    startListen () {
      var SpeechRecognition = self.SpeechRecognition || self.webkitSpeechRecognition
      var cust = this
      recognition = new SpeechRecognition()

      recognition.lang = 'en-US'
      recognition.continuous = true
      recognition.interimResults = true

      recognition.onresult = function (event) {
        // The SpeechRecognitionEvent results property returns a SpeechRecognitionResultList object
        // The SpeechRecognitionResultList object contains SpeechRecognitionResult objects.
        // It has a getter so it can be accessed like an array
        // The [last] returns the SpeechRecognitionResult at the last position.
        // Each SpeechRecognitionResult object contains SpeechRecognitionAlternative objects that contain individual results.
        // These also have getters so they can be accessed like arrays.
        // The [0] returns the SpeechRecognitionAlternative at position 0.
        // We then return the transcript property of the SpeechRecognitionAlternative object

        var words = event.results[0][0].transcript
        cust.directions = words
        console.log('Words:' + words)
        // console.log('Recognition result list:' + event.results[0][0].transcript)
        console.log('Confidence: ' + event.results[0][0].confidence)
      }

      recognition.onspeechend = function () {
        recognition.stop()
      }

      recognition.onerror = function (event) {
        cust.error = 'Error occurred in recognition: ' + event.error
      }

      recognition.start()
      console.log(recognition)
      console.log('Ready to recieve input.')
    },

    async send () {
      this.loading = true
      const tokens = await axios.get('/syntax', {
        params: {
          text: this.directions
        }
      })
      this.$store.commit('setTokens', tokens.data)
      this.$router.push('/view')
    }
  }
}
</script>
