<template>
    <div class="card horizontal h-100">
        <div class="header w-30 flex-fixed bg-highlight">
            <div class="background-icon">
                <icon icon="chart-line"></icon>
            </div>
        </div>
        <div class="content">
            <ul>
                <li>
                    <router-link :to="{name: 'dashboard', params: {id: dashboardId}}">
                        {{ dashboard.name }}
                    </router-link>
                    <a @click="removeDashboard(dashboardId)">[x]</a></li>
            </ul>
        </div>
    </div>
</template>

<script>
    import axios from "axios"


    export default {
        name: 'dashboard',
        props: {
            dashboardId: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                dashboard: {}
            }
        },
        methods: {
            async getDashboard() {
                const result = await axios.get("/plugins/dashboard/api/" + this.dashboardId)

                return result.data
            }
        },
        async mounted() {
            this.dashboard = await this.getDashboard()
        }
    }
</script>

<style lang="scss">

</style>
