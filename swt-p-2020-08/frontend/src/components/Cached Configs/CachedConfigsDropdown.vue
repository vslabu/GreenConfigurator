<template>
  <div class="btn-group span" role="group">
    <b-dropdown class="btn-block" :text="currentActiveConfig" menu-class="w-100">
      <b-dropdown-item
          v-for="(config, index) in cachedConfigs"
          :key="index"
          @click="loadConfig(config)"
      >
        {{ config.name }}
      </b-dropdown-item>
    </b-dropdown>
    <b-button v-on:click="gotoMono">
      Mono
    </b-button>
  </div>
</template>

<script>
export default {
  name: "CachedConfigsDropdown",
  props: {
    currentActiveConfig: {},
    cachedConfigs: {},
  },
  methods: {
    loadConfig(config){
      this.$emit('loadConfig', config);
    },
    gotoMono(){
      this.$emit('gotoMono');
    }
  }
}


</script>

<style scoped>

</style>