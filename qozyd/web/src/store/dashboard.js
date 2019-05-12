import axios from "axios"


export const CLEAR_DATA = "CLEAR_DATA"
export const SET_LOADING_STATE = "SET_LOADING_STATE"
export const SET_DASHBOARD_DATA = "SET_DASHBOARD_DATA"
export const SET_EDIT_MODE = "SET_EDIT_MODE"


export default {
    namespaced: true,
    state: {
        loading: false,
        editMode: true,
        dashboard: {},
    },
    getters: {
        tiles: state => {
            return state.dashboard.tiles || []
        },
        size: state => {
            return state.dashboard.size || {}
        }
    },
    mutations: {
        [SET_LOADING_STATE](state, value) {
            state.loading = value
        },
        [SET_DASHBOARD_DATA](state, dashboard) {
            state.dashboard = dashboard
        },
        [CLEAR_DATA](state) {
            state.dashboard = {}
        },
        [SET_EDIT_MODE](state, editMode) {
            state.editMode = editMode
        }
    },
    actions: {
        async loadDashboard({commit}, id) {
            commit(SET_LOADING_STATE, true)

            commit(CLEAR_DATA)

            const result = await axios.get("/plugins/dashboard/api/" + id)

            commit(SET_DASHBOARD_DATA, result.data)
            commit(SET_LOADING_STATE, false)
        },
        setEditMode({commit}, editMode) {
            commit(SET_EDIT_MODE, editMode)
        }
    }
}
