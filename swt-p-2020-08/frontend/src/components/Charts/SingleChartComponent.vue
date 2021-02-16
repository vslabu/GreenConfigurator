<template>
  <!--<updated-text-component :key="nfp['energy_consumption(Ws;<)']" :text="nfp['energy_consumption(Ws;<)']" />-->
  <div class="inLine">
    <H4>{{ dataName }}</H4>
    <canvas :id="chartID" width="250" height="400" style = "display:inline-block;"></canvas>
  </div>

</template>

<script>
import Chart from "chart.js";

export default {
  name: "SingleChartComponent",
  data: function(){
    return{
      //Diagramm
      chart: null,
    }
  },
  props: {
     //Dataset (Werte der einzelnen NFPs) fertig formatiert für das Diagramm
    dataSet:{},
      //Name des NFP Diagramms
    dataName:{},
      //Namen der einzelnen Konfigurationen
    chartLables:{},
      // Einheit der Skala
    unit :String,

    chartID: {}
  },

  mounted(){
    this.createChart(this.unit);
  },

  //Das Diagramm updaten, wenn sich die Daten ändern
  watch: {
  	dataSet: {
      handler: function () {
        // Änderung der Daten an Diagramm weitergeben
        if(JSON.stringify(this.chart.data.datasets[0].data) !== JSON.stringify(this.dataSet[0].data) ){
          this.chart.data.datasets[0].data = this.dataSet[0].data;

          // Diagramm updaten
          this.chart.update();
        }

      },
      deep: true
    },
    "chartLables": function(){
  	  this.chart.data.labels = this.chartLables;
  	  this.chart.update();
    }
  },
  methods: {
    createChart: function (unit) {
      var ctx = document.getElementById(this.chartID).getContext('2d');

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.chartLables,
          datasets: this.dataSet
        },
        options: {
          legend: {
            display: false
          },
          responsive: false,
          scales: {
            yAxes: [{
              ticks: {
                callback: function(value) {
                  var ret = value + " " + unit;
                  return ret;
                },
                beginAtZero: true
              }
            }]
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