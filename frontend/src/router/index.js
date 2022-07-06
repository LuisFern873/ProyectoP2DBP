import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Tareas from "../views/Tareas.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/register",
    name: "register",
    component: Register,
  },
  {
    path: "/empleados",
    name: "empleados",
    props: true,
    component: () => import(/* webpackChunkName: "empleados" */ "../views/Empleados.vue"),
  },

  {
    path: "/tareas",
    name: "tareas",
    component: Tareas,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
