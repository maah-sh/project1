<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title> ثبت نام ها به تفکیک جنسیت</v-card-title>
          <v-card-text>
            <canvas ref="pieChart" width="400" height="400"></canvas>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';

export default {
  data() {
    return {
      genderData: null,
      chart: null,
    };
  },
  mounted() {
    this.fetchGenderReport();
  },
  methods: {
    async fetchGenderReport() {
        await axios.get(`http://127.0.0.1:8000/registry/gender-report/`)
        .then(response => {
          console.log(response.data)
          this.genderData = response.data;
          this.renderChart();
        })
        .catch(error => {
          console.error('Error fetching data of gender report:', error);
        });
      },
    renderChart() {
      const ctx = this.$refs.pieChart.getContext('2d');

      if (this.chart) {
        this.chart.destroy(); 
      }

      this.chart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['مرد', 'زن'],
          datasets: [
            {
              data: [this.genderData.male_count, this.genderData.female_count],
              backgroundColor: ['#32E2C2', '#FF8A3E'],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
                datalabels: {
                  formatter: (value) => value === 0 ? '' : value,
                  color: "#fff",
                  font: {
                    family: "Yekan",
                    size: 24,
                    weight: "bold"
                  },
                  anchor: "center",
                  align: "center",
                },
                legend: {
                    labels: {
                        font: {
                        family: 'Yekan',
                        weight: 'bold',
                        },
                    },
                },
            },
        },
        plugins: [ChartDataLabels],
      });
    },
  },
};
</script>