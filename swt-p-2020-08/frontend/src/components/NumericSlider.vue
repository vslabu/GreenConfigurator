<template>
  <div>
    <input type="checkbox" checked disabled/>
    {{ option.display_name }} : {{ value }}
    <vue-slider v-model="value"
                :data="sliderValues"
                :width="250"
                @change="changeEnabled"
                :drag-on-click="true"
                style="display: inline-block; float: right; "
                :process-style="{ backgroundColor: '#9FD983' }"
    >
      <template v-slot:dot="{ value, focus }">
        <div :class="['custom-dot', { focus }]"></div>
      </template>
    </vue-slider>
  </div>

</template>

<script>
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/antd.css'

export default {
  name: "NumericSlider",
  components: {
    VueSlider
  },
  props: {
    option: {},
    konfigNr: {},
    valueProp: {}
  },

  data: function () {
    return {
      value: this.valueProp,
    };
  },
  computed: {

    // stepFunction aus JSON-Datei als eine math expression einlesen mit Parser:
    // => npm install expr-eval
    sliderValues: function () {
      var Parser = require('expr-eval').Parser;
      var parser = new Parser();
      var valuesArray = [];

      var i = this.option.minValue;

      var step = parser.parse(this.option.stepFunction);
      for (i; i <= this.option.maxValue;) {
        valuesArray.push(i);
        var variable = {};
        variable[this.option.name] = i;

        i = step.evaluate(variable);
      }
      //console.log(valuesArray);
      return valuesArray;
    }
  },
  methods: {
    //gibt an die Options Component weiter, dass sich der Wert geändert hat
    changeEnabled() {
      this.$emit('changeEnabled', {value: this.value, id: this.option.id});
    }
  },
  watch: {
    // Aktualisiert checked, wenn die Options Component die Option aktualisiert.
    // Dies passiert z.B. wenn die die Konfiguration optimiert wird.
    "valueProp": function () {
      this.value = this.valueProp
    },
  }

};

</script>

<style scoped>
.custom-dot {
  width: 100%;
  height: 100%;
  background-color: #37782C;
}

</style>