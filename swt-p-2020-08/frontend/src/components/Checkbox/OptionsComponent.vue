<template>
  <div>
    <div>
      <h4>Code: {{ code }}</h4>
      <OptionsSubtreeComponent
          v-for="option in featureModelRender"
          :key="option.id"
          :option="option"
          :featureModelSpeicher="featureModelSpeicher"
          :konfigNr="konfigNr"
          :type="option.type"
          @changeEnabled="changeEnabledAt($event)"
          style="width: 450px"
      />
    </div>
    <div>
      <!-- Komponente, die Anzeigt, ob die Konfiguration valide ist -->
      <UpdatedTextComponent :key="verified" :text="verified"/>
    </div>
    <div>
      <OptimizeButtonComponent :key="'optimize'"
                               :maxDepth="featureModelSpeicher.length"
                               :nfpNamen="nfp"
                               @optimizeByNfp="optimizeByNfp($event.nfp, $event.depth)"
                               @optimizeAllNfps="optimizeAllNfps($event)"
      />
    </div>
  </div>
</template>

<script>
//import CheckboxComponent from "@/components/CheckboxComponent";
import OptimizeButtonComponent from "@/components/Checkbox/OptimizeButtonComponent";
import axios from 'axios';
import UpdatedTextComponent from "@/components/UpdatedTextComponent";
import OptionsSubtreeComponent from "@/components/Checkbox/OptionsSubtreeComponent";



export default {
  name: "OptionsComponent",
  components: { OptionsSubtreeComponent, UpdatedTextComponent, OptimizeButtonComponent},
  data() {
    return {
      // speichert, ob die aktuelle konfiguration valide ist
      verified: false,
      featureModelSpeicher: this.featureModelSpeicherProp.map(o => ({...o})),
      // Eindeutiger Code der Konfiguration
      code: null,
    }
  },
  props: {
    // Liste der NFPs, die zum Rendern genutzt wird
    featureModelRender: {
      required: true
    },
    featureModelSpeicherProp: {},
    // Liste der NFPs
    // benötigt von OptimizeButtonComponent
    nfp: {},
    // Nummer der Konfiguration
    konfigNr: {},
    // Name des Models
    model: {},
  },
  watch:{
    "featureModelSpeicherProp" : function() {
      this.featureModelSpeicher = this.featureModelSpeicherProp.map(o => ({...o}))
    },
    "nameProp":function(){
      this.configName = this.nameProp;
    }
  },
  methods: {
    //Aktualisiert die features Liste, wenn eine änderung durchgeführt wurde
    changeEnabledAt: function (change) {
      if ('enabled' in change) {
        // Ein Boolean Wert wurde geändert
        //console.log(id, enabled)
        if (change.id != null && change.id >= 0) {
          this.$set(this.featureModelSpeicher[change.id], 'enabled', change.enabled);
        }
      } else {
        this.$set(this.featureModelSpeicher[change.id], 'value', change.value);
      }

      //Konfiguration überprüfen
      this.checkConfig();
    },

    //Gibt an die Parent-Componente weiter, dass sich die nfps geändert haben
    changeNFP: function (nfp) {
      this.$emit('changeNFP', nfp);
    },

    //Schickt die Konfiguration ans Backend um sie zu überprüfen
    checkConfig() {
      var postData = {
        config: this.featureModelSpeicher,
        model_name: this.model
      };

      const path = process.env.VUE_APP_SERVER_ADRESSE + 'api/checkAndCalculate';
      axios.post(path, postData)
          .then((res) => {
            var response = res.data.features;
            this.verified = response.verified;
            this.code = response.code;
            this.changeNFP(response.nfp);
          })
          .catch((error) => {
            console.error(error);
          });
    },

    //optimiert nach einem NFP
    optimizeByNfp(nfp, depth) {
      const path = process.env.VUE_APP_SERVER_ADRESSE + 'api/optimizeNFP';
      var postData = {
        config: this.featureModelSpeicher,
        depth: depth,
        nfp: nfp,
        model_name: this.model
      }
      axios.post(path, postData)
          .then((res) => {
            var response = res.data.features;
            this.verified = response.verified;
            this.code = response.code;
            this.changeNFP(response.nfp);
            this.featureModelSpeicher = response.features;
          })
          .catch((error) => {
            console.error(error);
          });
    },

    //Optimiere alle NFPs
    optimizeAllNfps(depth) {
      const path = process.env.VUE_APP_SERVER_ADRESSE + 'api/optimizeAll';
      var postData = {
        config: this.featureModelSpeicher,
        depth: depth,
        model_name: this.model
      }
      axios.post(path, postData)
          .then((res) => {
            var response = res.data.features;
            this.verified = response.verified;
            this.code = response.code;
            this.changeNFP(response.nfp);
            this.featureModelSpeicher = response.features;
          })
          .catch((error) => {
            console.error(error);
          });
    },
  },
}
</script>

<style scoped>
</style>