<template>
  <v-app light>
    <v-toolbar fixed>
      <v-toolbar-title v-text="title"></v-toolbar-title>
    </v-toolbar>
    <main>
      <v-container fluid>
        <nuxt />
      </v-container>
    </main>
  </v-app>
</template>

<script>
  export default {
    data () {
      return {
        title: 'ARTiculate'
      }
    }
  }
</script>
