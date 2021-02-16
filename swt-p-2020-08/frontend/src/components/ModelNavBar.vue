<template>

  <div>
    <b-dropdown
        id="dropdown-1"
        text="Model"
        menu-class="w-100"
        class="m-2">

      <b-dropdown-item
          v-for="(item, key) in modelNames"
          :key="key"
          :to="{params: {model: item} }"
          >

        {{ key + 1 + ": " }}{{ item }}

      </b-dropdown-item>

    </b-dropdown>
  </div>
</template>

<script>
import axios from "axios";

export default {

  name: "ModelNavBar",
  data() {
    return {
      isOpen: false,
      modelRoute: this.$route.params.model,
      modelNames: {},
    }

  },

  methods: {
    getModelNames() {

      const path = process.env.VUE_APP_SERVER_ADRESSE + 'api/getAllModelnames';
      axios.get(path)
          .then((res) => {
            this.modelNames = res.data.models;
          })
          .catch((error) => {
            console.error(error);
          });
    }
  },
  created() {
    this.getModelNames()
  }
}

</script>

<style scoped>

nav .menu-items {
  padding-top: 10px;
}

</style>