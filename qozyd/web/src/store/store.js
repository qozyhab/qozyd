import Vue from 'vue'
import Vuex from 'vuex'

import dashboard from "./dashboard"

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
      dashboard
  }
})
