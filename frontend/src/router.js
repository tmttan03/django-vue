import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      alias: "/dashboard",
      name: "dashboard",
      component: () => import("./components/Dashboard")
    },
    {
      path: "/value/:id",
      name: "value-details",
      component: () => import("./components/Value")
    },
    {
      path: "/principle/:id",
      name: "principle-details",
      component: () => import("./components/Principle")
    },
    {
      path: "/add",
      name: "add",
      component: () => import("./components/AddFeature")
    }
  ]
});