<template>
  <div class="container" id="vergleich" v-if="nfpNames != null">
    <div>
      <div class="row ">
        <ChartComponent class="form-inline"
                        :nfps="nfps"
                        :nfpNames="nfpNames"
                        :chart-lables="configName"
        />
      </div>

      <table>
        <tr>
          <td width="400">
            <div v-if="featureModelRender != null">
              <cached-configs-dropdown
                  :cached-configs="cachedConfigs"
                  :current-active-config="configName[0]"
                  @loadConfig="loadConfig($event, 0)"
                  @gotoMono="gotoMono(configName[0])"
              />
              <OptionsComponent
                  :key="('checkbox1', featureModelSpeicher[0].length)"
                  :featureModelRender="featureModelRender"
                  :featureModelSpeicherProp="featureModelSpeicher[0]"
                  :nfp="nfpNames"
                  :model="model"
                  :konfigNr="1"
                  @changeNFP="changeNFP($event, 0)"
              />
            </div>
          </td>
          <td width="400">
            <div v-if="featureModelRender != null">
              <cached-configs-dropdown
                  :cached-configs="cachedConfigs"
                  :current-active-config="configName[1]"
                  @loadConfig="loadConfig($event, 1)"
                  @gotoMono="gotoMono(configName[1])"
              />
              <OptionsComponent
                  :key="('checkbox2', featureModelSpeicher[1].length)"
                  :featureModelRender="featureModelRender"
                  :featureModelSpeicherProp="featureModelSpeicher[1]"
                  :nfp="nfpNames"
                  :model="model"
                  :konfigNr="2"
                  @changeNFP="changeNFP($event, 1)"
              />
            </div>
          </td>
        </tr>

      </table>
    </div>

  </div>

</template>

<script>

import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import OptionsComponent from "../components/Checkbox/OptionsComponent";
import ChartComponent from "../components/Charts/ChartComponent";
import axios from "axios";
import CachedConfigsDropdown from "@/components/Cached Configs/CachedConfigsDropdown";

Vue.use(BootstrapVue);

export default {
  name: 'VergleichView',
  components: {
    CachedConfigsDropdown,
    ChartComponent,
    OptionsComponent
  },
  data() {
    return {
      featureModelRender: [],
      featureModelSpeicher: [],
      nfps: [{}, {}],
      nfpNames: null,
      model: this.$route.params.model,

      configName: [this.configNameRouter1, this.configNameRouter2]
    }
  },
  props: {
    // Die FeatureModelle, die gegebenenfalls vom Router übergeben werden
    configNameRouter1: {},
    featureModelRouter1: {},
    configNameRouter2: {},
    featureModelRouter2: {},
    cachedConfigs: {}
  },
  methods: {
    //Läd das Feature Model
    getFeatureModel() {
      const path = process.env.VUE_APP_SERVER_ADRESSE + 'api/initFeatures';
      axios.post(path, {"model_name": this.model})
          .then((res) => {
            // Wenn vom Router Featuremodelle mitgegeben wurden, so werden diese benutzt, ansonsten wird das Standart Modell genutzt.
            if (this.featureModelRouter1 != null) {
              this.featureModelSpeicher[0] = this.featureModelRouter1;
            } else {
              this.featureModelSpeicher[0] = res.data.model.config;
              this.configName[0] = "Config 1";
            }
            if (this.featureModelRouter2 != null) {
              this.featureModelSpeicher[1] = this.featureModelRouter2;
            } else {
              this.featureModelSpeicher[1] = res.data.model.config;
              this.configName[1] = "Config 2";
            }

            this.featureModelRender = res.data.model.features;
            this.nfpNames = res.data.model.nfp;
          })
          .catch((error) => {
            console.error(error);
          });
    },

    changeNFP(nfp, index) {
      this.$set(this.nfps, index, nfp);
    },

    loadConfig(config, optionIndex) {
      axios.post(process.env.VUE_APP_SERVER_ADRESSE + '/api/loadConfiguration', {
        model_name: this.model,
        code: config.code
      })
          .then((res) => {
            //this.featureModelSpeicher[optionIndex] = res.data.features.features;
            this.$set(this.featureModelSpeicher, optionIndex, res.data.features.features);
            this.changeNFP(res.data.features.nfp, optionIndex);
          }).catch((error) => {
        console.log(error);
      })

      this.$set(this.configName, optionIndex, config.name);
      //this.configName[optionIndex] = config.name;
    },

    // Zur Mono Seite redirecten
    gotoMono(configName) {
      this.$router.push({
              name: 'mono',
              params: {
                configNameRouter: configName,
                cachedConfigs: this.cachedConfigs
              }
            });
    }
  },

  watch: {
    "$route.params.model": function () {
      //TODO: Was ist wenn ein falsches Featuremodel in der Adresszeile eingegeben wurde
      this.model = this.$route.params.model;
      this.getFeatureModel();
    }
  },

  created() {
    this.getFeatureModel();
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;

  color: #2c3e50;
  margin-top: 60px;
}

</style>

