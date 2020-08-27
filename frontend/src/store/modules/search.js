import {
    REQUEST_SEARCH_RESULTS,
    RECEIVE_SEARCH_RESULTS_SUCCESS,
    RECEIVE_SEARCH_RESULTS_FAILURE
} from '@/store/mutation-types'


const state = {
    loading: false,
    query_string: null,
    tab: 'All',
    search_results: null
}

const actions = {
    async searchRequest({ commit }) {
        try {
            commit(REQUEST_SEARCH_RESULTS);
            //const response = await fetch('https://jsonplaceholder.typicode.com/users');
            //const response = await fetch('https://jsonplaceholder.typicode.com/photos');
            const headers = new Headers({
                'accept': "application/json",
                'X-CSRFToken': "KINEmTrFLItYxeMfKYqJ0xNcJinCIlXv7qBqkCgFsocrW7CYlCJeY4VWUNxiwrTw"
            });
            const response = await fetch('http://127.0.0.1:8000/api/post/?page=1&page-size=10', {
                method: "GET",
                headers,
                
            });

            const res = await response.json();
            setTimeout(() => {
                commit(RECEIVE_SEARCH_RESULTS_SUCCESS, res);
            }, 2000);

        } catch (error) {
            commit(RECEIVE_SEARCH_RESULTS_FAILURE, error);
        }


    }
}

const mutations = {
    [REQUEST_SEARCH_RESULTS](state) {
        state.loading = true;
        console.log("inside request_search_results");
    },
    [RECEIVE_SEARCH_RESULTS_SUCCESS](state, results) {
        state.search_results = results;
        state.loading = false;
        console.log(results);
    },
    [RECEIVE_SEARCH_RESULTS_FAILURE](state, error) {
        state.search_results = null;
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