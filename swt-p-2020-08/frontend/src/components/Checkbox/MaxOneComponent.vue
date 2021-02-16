<template>
  <div>
      <!-- Erstellt eine Checkbox -->
    <!--
      <input type="radio"
             :id="'option' + option.id + konfigNr"
             v-model="active"
             :value="option.id"
             :disabled="!clickable"
             @change="changeActiveFeature()"
      />-->
    <input type="checkbox"
      :id="'option' + option.id + konfigNr"
      v-model="checked"
      :disabled="!clickable"
      @change="changeActiveFeature"
    />
      <label :for="'option' + option.id + konfigNr">{{ option.display_name }}</label>
    </div>
</template>

<script>
export default {
  name: "MaxOneComponent",
  props: {
    // Enthält alle Informationen zu der Option, wie z.B. name, id und checked
    "option": {},
    // Nummer der Konfiguration (z.B. 1 in MonoView oder 1 oder 2 in Vergleich)
    "konfigNr":{},
    // Die Id des features, das gerade aktiv ist
    "activeFeature": {},
    // Checkbox anklickbar
    "clickable": Boolean,
    // Checkbox aktiviert (genutzt, wenn die Konfiguration von außen geändert wird, z.B. wenn die Konfiguration optimiert wird)
    "enabled": Boolean
  },
  data: function (){
    return{
      // Wert der Checkbox: ist die Id der Checkbox, gdw. die Checkbox angeklick ist
      // Wird initial auf das zum Start aktive Feature gesetzt
      active: this.activeFeature,
      checked: this.activeFeature == this.option.id
    }
  },
  watch:{
    // Wenn sich das aktive Feature ändert, wird es auch innerhalb der Checkbox geändert, um sie gegebenenfalls zu deaktivieren
    "activeFeature" : function() {
      this.active = this.activeFeature;
      this.checked= this.activeFeature == this.option.id
    },
    "enabled" : function () {
      if(this.enabled){
        this.active = this.option.id;
        this.changeActiveFeature();
      }
    }
  },
  methods: {
    // gibt nach oben weiter, dass sich der Wert geändert hat
    // old ist das alte aktive Feature und new das neue
    changeActiveFeature(){
      if(this.checked){
        this.active = this.option.id
      } else {
        this.active = -1;
      }
      this.$emit('changeActiveFeature', {old: this.activeFeature, new: this.active});
    }
  }
}
</script>

<style scoped>

</style>
