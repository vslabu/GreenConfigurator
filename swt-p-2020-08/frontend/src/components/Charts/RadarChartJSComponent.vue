<template>
  <!--<updated-text-component :key="nfp['energy_consumption(Ws;<)']" :text="nfp['energy_consumption(Ws;<)']" />-->
  <div class="inLine">
    <canvas id="radar" width="500" height="400" style="display:inline-block;"></canvas>
  </div>

</template>

<script>
import Chart from "chart.js";

export default {
  name: "RadarChartJSComponent",
  data: function () {
    return {
      //Diagramm
      chart: null,

      chartBackgroundColors: [
        'rgba(159, 217, 131, 0.2)',
        'rgba(60, 179, 192, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
      chartBorderColors: [
        '#9FD983',
        '#3CB3C0',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ]
    }
  },
  props: {
    //Dataset (Werte der einzelnen NFPs) fertig formatiert für das Diagramm
    nfpNames: {},
    //Namen der einzelnen Konfigurationen
    nfpValues: {},
    // Name der einzelnen Konfigurationen
    labels: {}
  },

  mounted() {
    this.createChart();
  },

  //Das Diagramm updaten, wenn sich die Daten ändern
  watch: {
    nfpDataSet: {
      handler: function () {
        // Änderung der Daten an Diagramm weitergeben

        for (let i = 0; i < this.nfpValues.length; i++) {
          if (JSON.stringify(this.chart.data.datasets[i].data) !== JSON.stringify(this.nfpDataSet[i].data)) {
            this.chart.data.datasets[i].data = this.nfpDataSet[i].data;
            this.chart.data.datasets[i].label = this.nfpDataSet[i].label;

            // Diagramm updaten
            this.chart.update();
          }
        }

      },
      deep: true
    },

    nfpNames: {
      handler: function () {
        // Änderung der Daten an Diagramm weitergeben
        this.chart.data.datasets = this.nfpDataSet;
        this.chart.data.labels = this.chartLables;
        this.chart.update();
      },
      deep: true
    },
  },
  computed: {
    nfpDataSet: function () {
      let numberOfConfigurations = this.nfpValues.length;
      let numberOfNfps = this.nfpNames.length;

      let dataSet = new Array(numberOfConfigurations);
      for (let i = 0; i < numberOfConfigurations; i++) {

        let dataArray = new Array(numberOfNfps);

        for (let j = 0; j < numberOfNfps; j++) {

          let nfpName = this.nfpNames[j].name;
          let percentOfMax = (this.nfpValues[i][nfpName] - this.nfpNames[j].minimum) / (this.nfpNames[j].maximum - this.nfpNames[j].minimum) * 100;
          dataArray[j] = percentOfMax;
        }

        dataSet[i] = {
          label: this.labels[i],
          data: dataArray,
          backgroundColor: this.chartBackgroundColors[i],
          borderColor: this.chartBorderColors[i],
        }
      }
      return dataSet;
    },

    chartLables: function () {
      var nfpLength = this.nfpNames.length;

      var nfpNa = [];
      for (var i = 0; i < nfpLength; i++) {
        nfpNa.push(this.nfpNames[i].display_name);
      }
      return nfpNa;
    }
  },
  methods: {

    // Erstellt das Diagramm
    createChart: function () {
      var ctx = document.getElementById("radar").getContext('2d');

      this.chart = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: this.chartLables,
          datasets: this.nfpDataSet
        },
        options: {
          legend: {
            display: false
          },
          responsive: false,
          scale: {
            ticks: {
              max: 100,
              callback: function (value) {
                var ret = value + " %";
                return ret;
              },
              beginAtZero: true
            }
          }
        }
      });
    }
  }
}
</script>

<style scoped>
/*Sorgt dafür, dass die Diagramme alle in einer Zeile stehen*/
.inLine {
  float: left;
}
</style>