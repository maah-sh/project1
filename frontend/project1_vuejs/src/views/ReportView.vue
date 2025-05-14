<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
        <v-card>

          <v-card-title></v-card-title>

          <v-card-text></v-card-text>

          <GenderReport />
          <RegistrationDateReport
            v-for="year in jalaliYears"
            :key="year"
            :year="year"
           />


        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import GenderReport from '../components/GenderReport.vue';
import RegistrationDateReport from '../components/RegistrationDateReport.vue';

export default {
  components: {
    GenderReport,
    RegistrationDateReport,
  },
  data() {
    return {
      jalaliYears: [],
    };
  },
  mounted() {
    this.fetchJalaliYears();
  },
  methods: {
    async fetchJalaliYears() {
        await axios.get(`http://127.0.0.1:8000/registry/jalali-years/`)
        .then(response => {
          console.log(response.data)
          this.jalaliYears = response.data
        })
        .catch(error => {
          console.error('Error fetching jalali years:', error);
        });
      },
  }
};
</script>