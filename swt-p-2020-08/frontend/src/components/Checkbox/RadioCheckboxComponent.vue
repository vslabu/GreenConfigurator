<template>
  <div>
    <!-- Erstellt eine Checkbox -->
    <input type="radio"
           :id="'option' + option.id + konfigNr"
           v-model="active"
           :value="option.id"
           :disabled="!clickable"
           @change="changeActiveFeature()"
    />
    <label :for="'option' + option.id + konfigNr">{{ option.display_name }}</label>
  </div>
</template>

<script>
export default {
  name: "RadioCheckboxComponent",
  props: {
    // Enthält alle Informationen zu der Option, wie z.B. name, id und checked
    "option": {},
    // Nummer der Konfiguration (z.B. 1 in MonoView oder 1 oder 2 in Vergleich)
    "konfigNr": {},
    // Die Id des features, das gerade aktiv ist
    "activeFeature": {},
    // Checkbox anklickbar
    "clickable": Boolean,
    // Checkbox aktiviert (genutzt, wenn die Konfiguration von außen geändert wird, z.B. wenn die Konfiguration optimiert wird)
    "enabled": Boolean
  },
  data: function () {
    return {
      // Wert der Checkbox: ist die Id der Checkbox, gdw. die Checkbox angeklick ist
      // Wird initial auf das zum Start aktive Feature gesetzt
      active: this.activeFeature
    }
  },
  watch: {
    // Wenn sich das aktive Feature ändert, wird es auch innerhalb der Checkbox geändert, um sie gegebenenfalls zu deaktivieren
    "activeFeature": function () {
      this.active = this.activeFeature
    },
    "enabled": function () {
      if (this.enabled && this.active != this.option.id) {
        this.active = this.option.id;
        this.changeActiveFeature();
      }
    }
  },
  methods: {
    // gibt nach oben weiter, dass sich der Wert geändert hat
    // old ist das alte aktive Feature und new das neue
    changeActiveFeature() {
      this.$emit('changeActiveFeature', {old: this.activeFeature, new: this.active});
    }
  },
  mounted() {
    //console.log(this.enabled, this.active);
    if (this.enabled && this.activeFeature != this.option.id) {
      this.active = this.option.id;
      this.changeActiveFeature();
    }
  }
}
</script>

<style scoped>

</style>