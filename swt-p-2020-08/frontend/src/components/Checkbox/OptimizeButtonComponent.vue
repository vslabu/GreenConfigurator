<template>
  <div class="form-inline">

      Optimieren:

      <!-- Auswahl der Optimierungstiefe -->
      <select class="custom-select " v-model="depth" :key="'numberList'">
        <option v-for="number in numberList" v-bind:value="number" :key="'number' + number">
          {{ number }}
        </option>
      </select>

      <!-- Auswahl des zu optimierenden NFPs -->
      <select class="custom-select " v-model="nfpGewaehlt" :key="'nfpGewaehlt'">
        <option v-for="nfp in nfpNamen" v-bind:value="nfp.name" :key="nfp.name">
          {{ nfp.display_name }}
        </option>
        <option value="all" key="all">Alle NFPs optimieren</option>
      </select>

      <!-- Button zum Optimieren -->
      <b-button class="blueButton" v-on:click="optimize">Optimieren</b-button>
    </div>

</template>

<script>
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);

export default {
  name: "OptimizeButtonComponent",
  data() {
    return {
      // Aktuell gewählte Tiefe der Optimierung
      depth: 1,
      // Aktuell gewähltes NFP, auf das Optimiert werden soll
      nfpGewaehlt: this.nfpNamen[0].name,
    }
  },
  props: {
    // Maximale Tiefe der Optimierung
    'maxDepth': {},
    //Liste der NFP-Namen
    'nfpNamen': {}
  },
  computed: {
    // Liste der Zahlen von 1 bis maxDepth
    numberList() {
      var numbers = new Array(this.maxDepth);
      for (var i = 1; i <= this.maxDepth; i++) {
        numbers[i - 1] = i;
      }
      return numbers;
    },
  },
  methods: {
    // An die Options Component weitergeben, wie optimiert werden soll
    optimize() {
      if (this.nfpGewaehlt == "all") {
        this.$emit('optimizeAllNfps', this.depth);
      } else {
        this.$emit('optimizeByNfp', {nfp: this.nfpGewaehlt, depth: this.depth});
      }
    }
  },
}
</script>

<style scoped>

</style>