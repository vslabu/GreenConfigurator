<template>
  <div class="form-inline">
    <input class="form-control" type="text" v-model="code" placeholder="Code einfügen...">
    <b-button class="blueButton" @click="addConfig">Load</b-button>
  </div>
</template>

<script>
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);

export default {
  name: "KonfigurationLaden",
  components: {},

  data: function () {
    return {
      code: null
    }
  },
  methods: {
    addConfig(){
      this.$emit("addConfig", this.code);
    }
  },
}
</script>

<style scoped>

</style>