<template>
  <apexchart type="radar" height="500" :options="chartOptions" :series="series"></apexchart>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: "RadarChartComponent",
  props: {
    categ: {},
    nfpDa: {}
  },

  components: {apexchart: VueApexCharts,},

  data: function () {
    return {
      series: [{
        name: "config1",

        data: this.nfpDa,
      }],
      chartOptions: {
        chart: {
          height: 400,
          type: 'radar',
          dropShadow: {
            enabled: true,
            blur: 1,
            left: 1,
            top: 1
          }
        },
        title: {
          text: 'Radar Chart '
        },
        xaxis: {
          categories: this.categ
        },

      },
    }

  },

  watch: {
    nfpDa: {
      handler: function () {
        if (JSON.stringify(this.series[0].data) !== JSON.stringify(this.nfpDa)) {
          {
            this.series[0].data = this.nfpDa
          }
        }
      },
      deep: true,
      immediate: true,
    }
  }
}
</script>

<style scoped>

</style>