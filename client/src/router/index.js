import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/minifigs',
    name: 'Minifigs',
    component: () => import('../views/Minifigs.vue'),
  },
  {
    path: '/sets',
    name: 'Sets',
    component: () => import('../views/Sets.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
