<template>
  <div id="app">

    <header>
      <h1 class="text-center">GREEN CONFIGURATOR</h1>
      <ModelNavBar/>
    </header>


    <router-view/>
  </div>

</template>


<script>
import ModelNavBar from "@/components/ModelNavBar";

export default {
  name: 'app',
  components: {
    ModelNavBar
  },
}
</script>

<style>
.blueButton {
  background-color: #3CB3C0 !important;
  border-color: #2B7F88 !important;
}

.blueButton:hover {
  background-color: #2B7F88 !important;
}

.redTransparentButton {
  background: transparent;
  color: Red;
  border: transparent;
}

.redTransparentButton:hover {
  color: darkred;
  background-color: rgba(255, 255, 255, 0.2);
}

.greenTransparentButton {
  background: transparent;
  color: #64BB6A;
  border: transparent;
}

.greenTransparentButton:hover {
  color: #37782C;
  background-color: rgba(255, 255, 255, 0.2);
}

.text-center {
  color: green;
}

.btn-secondary {
  color: #fff;
  background-color: #3CB3C0 !important;
  border-color: #2B7F88 !important;
}

.btn-secondary:hover {
  background-color: #2B7F88 !important;
}

.btn-group.span {
  display: flex;
}


</style>
