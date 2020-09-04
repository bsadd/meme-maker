import {
    REQUEST_MEMES,
    RECEIVE_MEMES_SUCCESS,
    RECEIVE_MEMES_FAILURE
} from '@/store/mutation-types';
import axios from 'axios';


const state = {
    loading: false,
    query_string: null,
    tab: 'All',
    post_list: null
}

const actions = {
    async searchRequest({ commit }) {
            commit(REQUEST_MEMES);
            axios.get('http://127.0.0.1:8000/post/?page=1&page-size=10')
                .then(response => {
                    setTimeout(() => {
                        commit(RECEIVE_MEMES_SUCCESS, response.data.results);
                    }, 2000);
                }).catch(error => {
                    commit(RECEIVE_MEMES_FAILURE, error);
                })
    },
    
}

const mutations = {
    [REQUEST_MEMES](state) {
        state.loading = true;
    },
    [RECEIVE_MEMES_SUCCESS](state, results) {
        state.post_list = results;
        state.loading = false;
        console.log(results);
    },
    [RECEIVE_MEMES_FAILURE](state, error) {
        state.post_list = null;
        state.loading = false;
        console.log(error);
    }
}

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    modules: {
        
    }
}