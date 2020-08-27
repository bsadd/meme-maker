import Vue from 'vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';

const App = () =>
    import ('./App.vue')

Vue.config.productionTip = false

const ignoredMessage = "The .native modifier for v-on is only valid on components but it was used on <svg>.";

Vue.config.warnHandler = (message, vm, componentTrace) => {
    if (message !== ignoredMessage) {
        console.error(message + componentTrace);
    }
};

new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app')