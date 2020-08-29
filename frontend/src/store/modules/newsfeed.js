import {
    REQUEST_SEARCH_RESULTS,
    RECEIVE_SEARCH_RESULTS_SUCCESS,
    RECEIVE_SEARCH_RESULTS_FAILURE
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
            commit(REQUEST_SEARCH_RESULTS);
            axios.get('http://127.0.0.1:8000/post/?page=1&page-size=10')
                .then(response => {
                    setTimeout(() => {
                        commit(RECEIVE_SEARCH_RESULTS_SUCCESS, response.data.results);
                    }, 2000);
                }).catch(error => {
                    commit(RECEIVE_SEARCH_RESULTS_FAILURE, error);
                })


    }
}

const mutations = {
    [REQUEST_SEARCH_RESULTS](state) {
        state.loading = true;
    },
    [RECEIVE_SEARCH_RESULTS_SUCCESS](state, results) {
        state.post_list = results;
        state.loading = false;
        console.log(results);
    },
    [RECEIVE_SEARCH_RESULTS_FAILURE](state, error) {
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