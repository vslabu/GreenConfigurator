<template>
  <div>
    <!-- Erstellt eine Checkbox -->
    <input type="checkbox"
           :id="'option' + option.id + konfigNr"
           v-model="checked"
           :disabled="checkboxNotClickable"
           @change="changeEnabled"
    />
    <label :for="'option' + option.id + konfigNr">{{ option.display_name }}</label>
  </div>
</template>

<script>
export default {
  name: "CheckboxComponent",
  props: {
    // Enthält alle Informationen zu der Option, wie z.B. name, id und checked
    "option": {},
    // Nummer der Konfiguration (z.B. 1 in MonoView oder 1 oder 2 in Vergleich)
    "konfigNr": {},
    // Checkbox aktiviert
    "enabled": Boolean,
    // Checkbox anklickbar
    "clickable": Boolean
  },
  data: function () {
    return {
      // Speichert den Wert der Checkbox (Props sollen nicht direkt manipuliert werden, weshalb diese Variable verändert wird)
      // Dieser ist initial true, wenn die Option immer an sein soll
      checked: this.option.always_activated || this.enabled,
    };
  },
  computed: {
    // gibt zurück ob die Checkbox nicht anklickbar ist, also, ob sie deaktiviert ist oder nicht
    checkboxNotClickable: function () {
      // Checkbox wird dektiviert, wenn sie immer an sein soll oder als nicht clickable gekennzeichnet wurde
      var checkboxDisabled = this.option.always_activated || (!this.clickable);
      return checkboxDisabled;
    }
  },
  watch: {
    // Aktualisiert checked, wenn die Options Component die Option aktualisiert.
    // Dies passiert z.B. wenn die die Konfiguration optimiert wird.
    "enabled": function () {
      this.checked = this.enabled
      if (!this.enabled) {
        this.$emit('disableChildren');
      }
    },

    // Wenn die Checkbox auf notClickable gesetzt wird, so wird ihr Wert auf false gesetzt
    "checkboxNotClickable": function () {
      if (this.checkboxNotClickable) {
        this.checked = false;
        this.changeEnabled();
      }
    }
  },
  methods: {
    //gibt an die Options Component weiter, dass sich der Wert geändert hat
    changeEnabled() {
      this.$emit('changeEnabled', {enabled: this.checked, id: this.option.id});
    }
  },
  // gibt den initialen Wert der Checkbox nach oben weiter
  mounted() {
    if (this.option.always_activated) {
      this.changeEnabled();
    }
  }
};
</script>

<style scoped></style>
