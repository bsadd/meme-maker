import { convertToken, getNewToken } from '@/api/auth.api'
import { SET_ACCESS_TOKEN, SET_REFRESH_TOKEN } from '@/store/mutation-types'


const state = {
    access_token: null,
    refresh_token: null
};

const getters = {
    isLoggedIn(state) {
        return state.access_token !== null;
    }
};

const actions = {
    async exchangeSocialToken({ commit }, params) {
        try {
            const response = await convertToken(params);
            const data = response.data;
            console.log(data);

            commit(SET_ACCESS_TOKEN, data['access_token']);
            commit(SET_REFRESH_TOKEN, data['refresh_token']);
        } catch (error) {
            console.log(error);
        }
    },
    async loginWithCredentials({ commit, dispatch }, params) {
        try {
            const response = await getNewToken(params);
            const data = response.data;
            console.log(data);

            commit(SET_ACCESS_TOKEN, data['access_token']);
            commit(SET_REFRESH_TOKEN, data['refresh_token']);
        } catch (error) {
            // TODO: handle this error in login form
            let errorMessage = null;

            if (!error.response) {
                errorMessage = "Can't connect to server";
            } else {
                const statusCode = error.response.status;
                switch (statusCode) {
                    case 400:
                        errorMessage = 'Invalid credentials';
                        break;
                    case 404:
                        errorMessage = 'User not found';
                        break;
                    default:
                        errorMessage = 'Server error';
                        break;
                }
            }
            dispatch('error/sendErrorMessage', errorMessage, { root: true });
            return Promise.reject(error);
        }
    },
    async autoLogin({ commit }) {
        const token = localStorage.getItem('token');
        const params = {
            grant_type: 'refresh_token',
            client_id: process.env.VUE_APP_CLIENT_ID,
            client_secret: process.env.VUE_APP_CLIENT_SECRET,
            refresh_token: token
        };

        try {
            const response = await getNewToken(params);
            const data = response.data;
            console.log(data);

            commit(SET_ACCESS_TOKEN, data['access_token']);
            commit(SET_REFRESH_TOKEN, data['refresh_token']);
        } catch (error) {
            console.log(error);
            console.log(error.response);
        }
    },
    logOut({ commit }) {
        commit(SET_ACCESS_TOKEN, null);
        commit(SET_REFRESH_TOKEN, null);
    }
};

const mutations = {
    [SET_ACCESS_TOKEN](state, token) {
        state.access_token = token;
    },
    [SET_REFRESH_TOKEN](state, token) {
        state.refresh_token = token;
        localStorage.setItem('token', token);
    }
};

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
};