<template>
  <div class="card">
    <H5 class="card-header">Gespeicherte Konfigurationen</H5>
    <div class="card-body">
      <div
        v-for="(config, index) in savedConfigs"
        :key="index"
    >
      <div style="display:block; text-align:left; float:left;">
        {{ config.name }}
      </div>
      <div style="display:block; text-align:right;">

        <button
            class="greenTransparentButton"
            v-on:click="loadConfig(index)"
            title="Konfiguration Laden"
        >
          <!-- Pfeil Rechts Logo -->
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
               class="bi bi-arrow-right-square-fill" viewBox="0 0 16 16">
            <path
                d="M0 14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2a2 2 0 0 0-2 2v12zm4.5-6.5h5.793L8.146 5.354a.5.5 0 1 1 .708-.708l3 3a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708-.708L10.293 8.5H4.5a.5.5 0 0 1 0-1z"/>
          </svg>
        </button>
        <button
            class="greenTransparentButton"
            v-on:click="compareConfig(index)"
            title="Konfiguration mit aktueller vergleichen"
        >
          <!-- Split Screen Logo -->
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-layout-split"
               viewBox="0 0 16 16">
            <path
                d="M0 3a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3zm8.5-1v12H14a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1H8.5zm-1 0H2a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h5.5V2z"/>
          </svg>
        </button>
        <button
            v-on:click="deleteConfig(index)"
            class="redTransparentButton"
            title="Konfiguration löschen"
        >
          <!-- Mülleimer Logo -->
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash "
               viewBox="0 0 16 16">
            <path
                d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
            <path fill-rule="evenodd"
                  d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
          </svg>
        </button>
      </div>


    </div>
    <konfiguration-laden
        @addConfig="addConfig($event)"
    />
    </div>

  </div>
</template>

<script>
import KonfigurationLaden from "@/components/KonfigurationLaden";
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);

export default {
  name: "CachedConfigsComponent",
  components: {KonfigurationLaden},
  props: {
    savedConfigs: {}
  },
  methods: {
    // Löscht Config aus der SavedConfigs-Liste
    deleteConfig(index) {
      this.savedConfigs.splice(index, 1);
    },

    // Lädt die gewählte Konfiguration in die Options Component
    loadConfig(index) {
      this.$emit('loadConfig', index);
    },

    addConfig(config) {
      this.$emit('addConfig', config);
    },

    compareConfig(index) {
      this.$emit('compareConfig', index);
    }
  }
}
</script>

<style scoped>
.border {
  border-style: solid
}
</style>