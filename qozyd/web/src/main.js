import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import {library} from '@fortawesome/fontawesome-svg-core'
import {
    faCogs,
    faPlusSquare,
    faPowerOff,
    faPalette,
    faFont,
    faSlidersH,
    faChartBar,
    faToggleOn,
    faSortNumericUp,
    faChartLine,
    faEnvelope,
    faPlusCircle,
    faTrash,
    faEllipsisV,
    faPlayCircle,
    faPlay,
    faStopCircle,
    faCheck,
    faTimes,
    faSearch,
    faSpinner,
    faFlask,
    faEdit,
    faCode,
    faCodeBranch,
    faArrowRight,
    faSync,
    faCompass
} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

import Overview from './components/views/overview/Overview.vue'
import Bridges from './components/views/bridges/Bridges.vue'
import BridgeSettings from './components/views/bridges/BridgeSettings.vue'
import BridgeSettingsJson from "./components/views/bridges/BridgeSettingsJson.vue";
import BridgeSettingsForm from "./components/views/bridges/BridgeSettingsForm.vue";
import Dashboard from './components/views/dashboard/Dashboard.vue'
import Things from './components/views/things/Things.vue'
import Rules from "./components/views/rules/Rules.vue";
import Rule from "./components/views/rule/Rule.vue";


import ClickOutside from "./directive/click-outside.js"
import Popper from "./directive/popper.js"

import './main.scss'
import 'c3/c3.css'
import store from './store/store'

Vue.config.productionTip = false

library.add(
    faCogs, faPlusSquare, faPowerOff, faPalette, faFont, faSlidersH, faChartBar, faToggleOn, faSortNumericUp,
    faChartLine, faEnvelope, faPlusCircle, faTrash, faEllipsisV, faPlayCircle, faPlay, faStopCircle, faCheck, faTimes,
    faSearch, faSpinner, faFlask, faEdit, faCode, faCodeBranch, faArrowRight, faSync, faCompass
)
Vue.component('icon', FontAwesomeIcon)

Vue.directive("click-outside", ClickOutside)
Vue.directive("popper", Popper)

Vue.use(VueRouter)

const routes = [
    {path: '/', component: Overview, name: "overview"},
    {path: '/bridges', component: Bridges, name: "bridges"},
    {path: '/bridges/:bridgeId/settings', props:true, component: BridgeSettings, children: [
            {
                path: "",
                name: "bridge_settings",
                component: BridgeSettingsJson,
                props: true
            },
            {
                path: "form",
                name: "bridge_settings.form",
                component: BridgeSettingsForm,
                props: true
            },
        ]},
    {path: '/things', component: Things, name: "things"},
    {path: '/rules', component: Rules, name: "rules"},
    {path: '/rules/:ruleId', component: Rule, props: true, name: "rule"},
    {path: '/plugins', component: Overview, name: "plugins"},
    {path: '/:id', component: Dashboard, props: true, name: "dashboard"}
]

const router = new VueRouter({
    routes
})

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
