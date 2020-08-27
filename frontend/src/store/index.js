import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import error from './modules/error'
import newsfeed from './modules/newsfeed'

Vue.use(Vuex);

const store = new Vuex.Store({
    modules: {
        auth,
        newsfeed,
        error
    },
    strict: process.env.NODE_ENV !== 'production'
});

export default store;