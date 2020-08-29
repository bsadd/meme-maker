import { SET_ERROR, RESET_ERROR } from '@/store/mutation-types';

const state = {
    show: false,
    message: null
}

const mutations = {
    [SET_ERROR](state, msg) {
        state.show = true;
        state.message = msg;
    },
    [RESET_ERROR](state) {
        state.show = false;
        state.message = null;
    }
}

const actions = {
    async sendErrorMessage({ commit }, msg) {
        commit(SET_ERROR, msg);
        setTimeout(() => commit(RESET_ERROR), 4000);
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}