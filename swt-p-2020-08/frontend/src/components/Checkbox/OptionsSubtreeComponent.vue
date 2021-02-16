<template>
  <div>
    <!-- ########################## Checkbox in dieser Ebene ausgeben ########################## -->
    <div
        style="padding-right:15px;"
        v-if="option.type == 'numeric'"
    >
      <!-- Sliderm, wenn die Option numerische Werte annehmen kann -->
      <numeric-slider
          :key="option.id"
          :konfig-nr="konfigNr"
          :option="option"
          :valueProp="featureModelSpeicher[option.id].value"
          @changeEnabled="changeThisEnabled($event)"
      />
    </div>
    <div
        v-else-if="mode == 'CHOOSE_ONE'"
    >
      <!-- Runde Checkbox, wenn die Option innerhalb einer CHOOSE_ONE Umgebung ist -->
      <radio-checkbox-component
          :key="option.id"
          :konfig-nr="konfigNr"
          :option="option"
          :activeFeature="activeFeatureThis"
          :clickable="clickable"
          :enabled="featureModelSpeicher[option.id].enabled"
          @changeActiveFeature="changeActiveFeature($event)"
      />
    </div>
    <div
        v-else-if="mode == 'CHOOSE_MAX_ONE'"
    >
      <!-- Eckige Checkbox, wenn die Option innerhalb einer CHOOSE_MAX_ONE Umgebung ist -->
      <max-one-component
          :key="option.id"
          :konfig-nr="konfigNr"
          :option="option"
          :activeFeature="activeFeatureThis"
          :clickable="clickable"
          :enabled="featureModelSpeicher[option.id].enabled"
          @changeActiveFeature="changeActiveFeature($event)"
      />
    </div>
    <div
        v-else
    >
      <!-- Eckige Checkbox, sonst -->
      <checkbox-component
          :key="option.id"
          :konfig-nr="konfigNr"
          :option="option"
          :enabled="featureModelSpeicher[option.id].enabled"
          :clickable="clickable"
          @changeEnabled="changeThisEnabled($event)"
          @disableChildren="disableChildren()"
      />
    </div>

    <!-- ########################## Kinder ausgeben ########################## -->
    <div
        style="padding-left:15px;"
        v-if="option.children_type != null "
    >
      <OptionsSubtreeComponent
          v-for="childOption in option.children"
          :key="childOption.id"
          :mode="option.children_type"
          :option="childOption"
          :konfig-nr="konfigNr"
          :feature-model-speicher="featureModelSpeicher"
          :clickable="featureModelSpeicher[option.id].enabled"
          :active-feature-this="activeFeatureChild"
          @changeEnabled="changeEnabled($event)"
          @changeActiveFeature="changeActiveFeatureChild($event.old, $event.new)"
      />
    </div>
  </div>
</template>

<script>
import CheckboxComponent from "@/components/Checkbox/CheckboxComponent";
import RadioCheckboxComponent from "@/components/Checkbox/RadioCheckboxComponent";
import MaxOneComponent from "@/components/Checkbox/MaxOneComponent";
import NumericSlider from "@/components/NumericSlider";


export default {
  name: "OptionsSubtreeComponent",
  components: {MaxOneComponent, CheckboxComponent, RadioCheckboxComponent, NumericSlider},
  props: {
    // Modus dieses Subtrees ("CHOOSE_MULTIPLE", "CHOOSE_ONE", "CHOOSE_MAX_ONE"
    "mode": String,
    // Option, das in dieser Ebene gerendert wird
    "option": {},
    // Nummer der Konfiguration
    "konfigNr": {},
    // Liste des Feature Models, in dem alle Werte gespeichert werden
    "featureModelSpeicher": {},
    // Ist das Feature aktuell anklickbar?
    "clickable": Boolean,
    // Aktives Feature auf dieser Ebene (Nur genutzt innerhalb einer CHOOSE_ONE Umgebung)
    "activeFeatureThis": {},
  },
  data: function () {
    return {
      // Aktives Feature in der Ebene der Kinder (Nur genutzt, wenn die Ebene der Kinder eine CHOOSE_ONE Umgebung ist
      activeFeatureChild: null
     // activeFeatureChild: -1
    }
  },
  methods: {
    // Die Checkbox dieses Subtrees wurde geändert
    changeThisEnabled(change) {
      // Aktualisiert den Wert des Features
      this.$emit('changeEnabled', change);

      // Wenn die Kinder eine CHOOSE_ONE Umgebung sind, muss diese Ebene zusätzlich aktualisiert werden
      if (this.option.children_type == "CHOOSE_ONE") {
        if (!change.enabled) {
          // Wenn die Option in dieser Ebene ausgeschalten wird, so muss die CHOOSE_ONE Umgebung in der Ebene darunter
          // so gesetzt werden, dass kein Feature aktiviert ist

          // Das aktuell aktivierte Feature dieser Ebene ausschalten
          this.$emit('changeEnabled', {enabled: false, id: this.activeFeatureChild});
          // Das aktive Feature auf 0 setzen
          this.activeFeatureChild = -1;
          } else {
          // Wenn die Option eingeschalten wurde, so muss wieder in der Ebene darunter ein Kind ausgewählt werden,
          // da immer eines Aktiv sein muss
          this.initActiveFeature()
          }
        }
      },

      // Leitet eine änderung aus einer tiefer liegenden Ebene nach oben weiter
    changeEnabled(change) {
      this.$emit('changeEnabled', change);
    },

    // Wenn diese Ebene in einer CHOOSE_ONE Umgebung liegt, so wird der Ebene darüber mitgeteilt, dass sich das
    // aktive Feature geändert hat
    changeActiveFeature(change) {
      this.$emit('changeActiveFeature', change);
      if (this.option.children_type == "CHOOSE_ONE" || this.option.children_type == "CHOOSE_MAX_ONE") {
        if (change.new == this.option.id) {
          this.enableChildren();
        }
      }
    },

    // Wenn die Ebene der Kinder eine CHOOSE_ONE Umgebung ist und sich darin etwas geändert hat, so wird diese Änderung
    // allen Kindern mitgeteilt und die Änderung als normale Boolean Änderung nach oben weiter gegeben.
    changeActiveFeatureChild(oldFeature, newFeature) {
      // Aktives Feature der Kinder Ebene ändern, um der Ebene die Änderung mitzuteilen
      this.activeFeatureChild = newFeature;
      // Altes Feature ausschalten, falls es ein existentes Feature ist
      if (oldFeature != -1) {
        this.$emit('changeEnabled', {enabled: false, id: oldFeature});
      }
      // Neues anschalten
      this.$emit('changeEnabled', {enabled: true, id: newFeature});
    },

    // Wenn die Ebene aktiviert ist und die Kinder Ebene eine CHOOSE_ONE Umgebung ist, so wird als aktives Kind
    // das erste Kind ausgewählt
    initActiveFeature() {
      if (this.featureModelSpeicher[this.option.id].enabled && this.option.children_type == "CHOOSE_ONE") {
        this.activeFeatureChild = this.option.children[0].id;
        this.changeEnabled({enabled: true, id: this.option.children[0].id});
      }
    },

    disableChildren() {
      // Wenn die Option in dieser Ebene ausgeschalten wird, so muss die CHOOSE_ONE Umgebung in der Ebene darunter
      // so gesetzt werden, dass kein Feature aktiviert ist

      // Das aktuell aktivierte Feature dieser Ebene ausschalten
      this.$emit('changeEnabled', {enabled: false, id: this.activeFeatureChild});
      // Das aktive Feature auf 0 setzen
      this.activeFeatureChild = -1;
    },

    enableChildren() {
      // Wenn die Option eingeschalten wurde, so muss wieder in der Ebene darunter ein Kind ausgewählt werden,
      // da immer eines Aktiv sein muss
      this.initActiveFeature()
    },
  },

    watch:{
    // Wenn sich das aktive Feature ändert, wird es auch innerhalb der Checkbox geändert, um sie gegebenenfalls zu deaktivieren
    "activeFeatureThis" : function() {
      if(this.activeFeatureThis != this.option.id){
        this.disableChildren();
        }
      }
    },

  // Das aktive Feature wird initialisiert, falls es sich bei den Kindern um eine CHOOSE_ONE Umgebung handelt
  created() {
    this.initActiveFeature();
  }
}
</script>

<style scoped>

</style>