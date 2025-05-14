<template>
  <v-app>
    <Navbar-links />

    <v-main>
      <router-view/>
    </v-main>

  </v-app>
</template>

<script>

import NavbarLinks from './components/NavbarLinks.vue';

export default {
  components: {
    NavbarLinks,
  },
};

</script>


<style scoped>
@font-face {
  font-family: 'Yekan';
  src: url('./assets/fonts/BYekan.eot') format('eot'),
       url('./assets/fonts/BYekan.woff') format('woff'),
       url('./assets/fonts/BYekan.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

.v-application {
  font-family: 'Yekan', sans-serif !important;
}
</style>
