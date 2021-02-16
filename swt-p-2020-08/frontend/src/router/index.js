import Vue from "vue";
import VueRouter from "vue-router";
import Mono from "../views/MonoView.vue";
import Vergleich from "../views/VergleichView.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",  redirect: '/HSQL DB/mono'
    //name: "Choose Configuration",
    //component: Mono
  },
  {
    path: "/:model/mono",
    name: "mono",
    component: Mono
  },
  {
    path: "/:model/compare",
    name: "compare",
    component: Vergleich,
    props:true
  },
  { path: "/index.html", redirect: "/" }
];

const router = new VueRouter({
  base: "",
  routes
});

export default router;
