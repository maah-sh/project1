<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card color="#EAFAF1">
            <v-card-title >گزارش سال {{year}} :</v-card-title>
          </v-card>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title > ثبت نام های ماهانه در  {{year}}</v-card-title>
            <v-card-text>
                <canvas ref="totalChart"></canvas>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="12" md="8">
            <v-row>
                <v-col cols="12" md="12" v-for="(monthData, month) in data" :key="month">
                    <v-card>
                        <v-card-title>ثبت نام های هفتگی در   {{ monthNames[parseInt(month) -1] }} {{year}}</v-card-title>
                        <v-card-text >
                            <canvas ref="weekCharts" :data-month="month"></canvas>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
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
      data: null,
      totalChartInstance: null,
      weekChartInstances: [],
      monthNames: [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
      ],
    };
  },
  props: {
    year: {
      required: true,
    },
  },
  mounted() {
    this.fetchRegistrationDateReport(this.year);
  },
  methods: {
    async fetchRegistrationDateReport(jalali_year) {
      await axios.get(`http://127.0.0.1:8000/registry/registration-date-report/${jalali_year}/`)
      .then(response => {
        console.log(response.data)
        this.data = response.data;
        this.createTotalChart();
        this.$nextTick(() => { 
          this.createWeekCharts();
        });
      })
      .catch(error => {
        console.error('Error fetching data of registration date:', error);
      });
    },
    createTotalChart() {
      
        const months = [
        "فروردین"
        , "اردیبهشت"
        , "خرداد"
        , "تیر"
        , "مرداد"
        , "شهریور"
        , "مهر"
        , "آبان"
        , "آذر"
        , "دی"
        , "بهمن"
        , "اسفند"
        ];
        const totalCounts = Object.values(this.data).map((month) => month.total_count);

      const ctx = this.$refs.totalChart.getContext('2d');
      this.totalChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: months,
          datasets: [
            {
              label: 'تعداد ثبت',
              data: totalCounts,
              backgroundColor: "#097969",
            },
          ],
        },
        options: {
          scales: {
            x: {
                stacked: true,
                grid: { display: false },
                ticks: { font: { size: 18, family: 'Yekan' }, padding: 15}
              },
            y: {
              beginAtZero: true,
              grid: { display: false },
              ticks: {
                    stepSize: 1, 
                    precision: 0,
                },
            },
          },
          plugins: {
                datalabels: {
                    anchor: 'center',
                    align: 'center',
                    color: "#fff",
                    formatter: (value) => value === 0 ? '' : Math.round(value),
                    font: {
                    weight: 'bold',
                    family: 'Yekan',
                    size: 18,
                    },
                },
                legend: {
                    labels: {
                        font: {
                        family: 'Yekan',
                        size: 14,
                        weight: 'bold',
                        },
                    },
                },
            },
        },
        plugins: [ChartDataLabels],
      });
    },
    createWeekCharts() {
      const weekCharts = this.$refs.weekCharts;
      if (!Array.isArray(weekCharts)) {
        return;
      }
      weekCharts.forEach((canvas) => {
        const month = canvas.dataset.month;
        const weekData = this.data[month].weeks;

        const weeks = [
        "هفته اول"
        , "هفته دوم"
        , "هفته سوم"
        , "هفته چهارم"
        ];

        const maleCounts = Object.values(weekData).map((week) => week.male_count);
        const femaleCounts = Object.values(weekData).map((week) => week.female_count);

        const ctx = canvas.getContext('2d');
        const chartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: weeks,
            datasets: [
              {
                label: 'مرد',
                data: maleCounts,
                stack: 'Stack 0',
                backgroundColor: "#36A2EB",
              },
              {
                label: 'زن',
                data: femaleCounts,
                stack: 'Stack 0',
                backgroundColor: "#FF6384",
              },
            ],
          },
          options: {
            scales: {
              x: {
                stacked: true,
                grid: { display: false },
                ticks: { font: { size: 18, family: 'Yekan' }, padding: 15}
              },
              y: {
                beginAtZero: true,
                stacked: true,
                grid: { display: false },
                ticks: {
                  stepSize: 1, 
                  precision: 0,
                },
              },
            },
            plugins: {
                datalabels: {
                    anchor: 'center',
                    align: 'center',
                    color: "#fff",
                    formatter: (value) => value === 0 ? '' : Math.round(value),
                    font: {
                    weight: 'bold',
                    family: 'Yekan',
                    size: 18,
                    },
                },
                legend: {
                    labels: {
                        font: {
                        family: 'Yekan',
                        size: 14,
                        weight: 'bold',
                        },
                    },
                },
            },
          },
          plugins: [ChartDataLabels],
        });
        this.weekChartInstances.push(chartInstance);
      });
    },
  },
};
</script>


