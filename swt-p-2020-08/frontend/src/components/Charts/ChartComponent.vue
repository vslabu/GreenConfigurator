<template>
  <div>
    <single-chart-component
        v-for="(nfpName, index) in nfpNames"
        :key="index"
        :data-name="nfpName.display_name"
        :chart-lables="chartLables"
        :unit="nfpName.unit"
        :data-set="nfpDataset[nfpName.name]"
        :chart-i-d="index"
    />
    <radar-chart-j-s-component
        :nfp-names="nfpNames"
        :nfp-values="nfpData"
        :labels="chartLables"
    />
  </div>
</template>

<script>
import SingleChartComponent from "./SingleChartComponent";
//import RadarChartComponent from "./RadarChartComponent";
import RadarChartJSComponent from "@/components/Charts/RadarChartJSComponent";

export default {
  name: "ChartComponent",
  components: {RadarChartJSComponent, SingleChartComponent},
  data: function () {
    return {
      // Werte der nfps
      nfpData: this.nfps,
      //Farben der Balken im Diagramm
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
    nfps: {},
    nfpNames: {},
    chartLables: {}
  },
  computed: {
    //Liste der NFP-Namen
    /*nfpNamensListe: function () {
      return Object.keys(this.nfps[0]);
    },*/

    //Generiert eine Liste, die für jedes NFP das passende Dataset generiert.
    // Man findet das Dataset mit nfpDataset["nfpname"]
    nfpDataset: function () {
      var nfpDataset = {};
      for (var nfpName of this.nfpNames) {
        nfpDataset[nfpName.name] = new Array(1);
        var nfpLength = this.nfpData.length;
        var dataList = new Array(nfpLength);
        for (var i = 0; i < nfpLength; i++) {
          //console.log(this.nfpData[i][nfpName.name])
          dataList[i] = this.nfpData[i][nfpName.name];
        }
        nfpDataset[nfpName.name][0] = {
          "label": nfpName.display_name,
          "data": dataList,
          "backgroundColor": this.chartBackgroundColors,
          "borderColor": this.chartBorderColors,
          "borderWidth": 1
        }

      }
      return nfpDataset;
    },


    // Liste der Namen der nfps
    /*
    nfpNa: function () {
      var nfpLength = this.nfpNames.length;

      var nfpNa = [];
      for (var i = 0; i < nfpLength; i++) {
        nfpNa.push(this.nfpNames[i].display_name);
      }
      return nfpNa;
    },

    dataLi: function () {

      var dataLi = new Array();

      for (var nfpName of this.nfpNames) {

        dataLi.push(this.nfpDataset[nfpName.name][0].data[0]);

      }
      return dataLi;
    }*/
  }
}

</script>

<style scoped>

</style>