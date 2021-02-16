<template>
  <div id="mono" class="row justify-content-center">
    <div class="row justify-content-start">
      <div>
        <cached-configs-component
            :saved-configs="cachedConfigs"
            @loadConfig="loadConfig($event)"
            @addConfig="addConfig($event)"
            @compareConfig="compareConfig($event)"
        />
      </div>


      <div class="row align-content-center" id="checkbox"
           v-if="featureModelRender != null"
      >
        <div>
          <div class="form-inline">
            <h3>
              Name:
              <input class="form-control" type="text" v-model="configName">
              <b-button class="blueButton" v-on:click="saveConfig">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-save2"
                     viewBox="0 0 16 16">
                  <path
                      d="M2 1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H9.5a1 1 0 0 0-1 1v4.5h2a.5.5 0 0 1 .354.854l-2.5 2.5a.5.5 0 0 1-.708 0l-2.5-2.5A.5.5 0 0 1 5.5 6.5h2V2a2 2 0 0 1 2-2H14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h2.5a.5.5 0 0 1 0 1H2z"/>
                </svg>
              </b-button>
            </h3>
          </div>
          <div>

            <OptionsComponent
                :key="featureModelSpeicher.length"
                :featureModelRender="featureModelRender"
                :featureModelSpeicherProp="featureModelSpeicher"
                :nfp="nfpNames"
                :model="model"
                :konfigNr="1"
                @changeNFP="changeNFP($event)"

                ref="optionsComponent"
            />
          </div>
        </div>
      </div>


      <div id="chart"
           v-if="nfpNames != null"
      >
        <ChartComponent
            :nfps="nfps"
            :nfpNames="nfpNames"
            :chart-lables="[configName]"
        />
      </div>

    </div>
  </div>


</template>

<script>

import OptionsComponent from "../components/Checkbox/OptionsComponent";
import ChartComponent from "../components/Charts/ChartComponent";
import axios from "axios";
import CachedConfigsComponent from "@/components/Cached Configs/CachedConfigsComponent";
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


Vue.use(BootstrapVue);

export default {
  name: 'MonoView',
  components: {
    CachedConfigsComponent,
    ChartComponent,
    OptionsComponent,
  },
  data() {
    return {
      featureModelRender: null,
      featureModelSpeicher: null,
      nfps: [{}],
      nfpNames: null,
      model: this.$route.params.model,

      configName: "Config 1",
      cachedConfigs: []
    }
  },
  methods: {
    //Läd das Feature Model
    getFeatureModel() {
      const path = process.env.VUE_APP_SERVER_ADRESSE + 'api/initFeatures';
      axios.post(path, {"model_name": this.model})
          .then((res) => {
            this.featureModelSpeicher = res.data.model.config;
            this.featureModelRender = res.data.model.features;
            this.nfpNames = res.data.model.nfp;

            // Gespeicherte Konfigurationen laden
            this.cachedConfigs = [];
            for (let config of res.data.model.bestConfigs) {
              this.cachedConfigs.push({name: config.display_name, code: config.code});
            }
          })
          .catch((error) => {
            console.error(error);
          });
    },

    changeNFP(nfps) {
      this.$set(this.nfps, 0, nfps);
    },

    // Speichert Konfiguration
    saveConfig() {
      let isInList = false;
      for (let oldConfig of this.cachedConfigs) {
        if (oldConfig.name === this.configName) {
          oldConfig.code = this.$refs.optionsComponent.code;
          isInList = true;
          break;
        }
      }
      if (!isInList) {
        console.log(this.$refs.optionsComponent);
        this.cachedConfigs.push({name: this.configName, code: this.$refs.optionsComponent.code});
      }
    },

    // Lädt die Konfiguration in die Options Component
    loadConfig(index) {
      let config = this.cachedConfigs[index];

      axios.post(process.env.VUE_APP_SERVER_ADRESSE + '/api/loadConfiguration', {
        model_name: this.model,
        code: config.code
      })
          .then((res) => {
            this.featureModelSpeicher = res.data.features.features;
            this.changeNFP(res.data.features.nfp);
          }).catch((error) => {
        console.log(error);
      })

      this.configName = config.name;
      this.$refs.optionsComponent.code = config.code;
    },

    // Fügt Konfig hinzu, falls diese Valide ist
    addConfig(code) {
      let response = null;
      axios.post(process.env.VUE_APP_SERVER_ADRESSE + '/api/loadConfiguration', {model_name: this.model, code: code})
          .then((res) => {
            response = res.data.features;
            if (response.verified) {
              // Der Eingegebene Code gehört zu einer Validen Konfiguration

              //Konfiguration laden
              console.log(this.featureModelSpeicher);
              this.featureModelSpeicher = response.features;
              console.log(this.featureModelSpeicher);
              this.changeNFP(response.nfp);

              // Konfiguration mit nächstem freien generischen "Config"i Namen benennen
              let i = 1;
              let isInList = false;
              //Berechnet das nächste freie i
              do {
                isInList = false;
                for (let oldConfig of this.cachedConfigs) {
                  if ("Config " + i === oldConfig.name) {
                    i++;
                    isInList = true;
                  }
                }
              } while (isInList)

              this.configName = "Config " + i;
              this.$refs.optionsComponent.code = code;
            }
          }).catch((error) => {
        console.log(error);
      })
    },

    // Lässt aktuell offene Konfiguration mit der gewählten Konfiguration auf der Compare Seite vergleichen
    compareConfig(index) {
      this.saveConfig()

      //Konfiguration aus Liste laden
      let config = this.cachedConfigs[index];
      let featureModel2 = null;


      axios.post(process.env.VUE_APP_SERVER_ADRESSE + '/api/loadConfiguration', {
        model_name: this.model,
        code: config.code
      })
          .then((res) => {
            featureModel2 = res.data.features.features;

            // Leitet auf die Compare Ansicht weiter
            this.$router.push({
              name: 'compare',
              params: {
                configNameRouter1: this.configName,
                featureModelRouter1: this.$refs.optionsComponent.featureModelSpeicher,
                configNameRouter2: config.name,
                featureModelRouter2: featureModel2,
                cachedConfigs: this.cachedConfigs
              }
            });
          }).catch((error) => {
        console.log(error);
      })
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

.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: 10px;
  margin-left: 10px;
}
</style>

