<template>
    <div class="overview">
        <transition name="fade">
            <div class="row" v-if="dashboards.length > 0">
                <div class="col-12">
                    <h2>Dashboards</h2>
                </div>

                <div class="col-sm-6 col-lg-4 col-xl-3 overview-card" v-for="dashboard in dashboards" :key="dashboard.id">
                    <dashboard :dashboard-id="dashboard"></dashboard>
                </div>
            </div>
        </transition>

        <transition name="fade">
            <div class="row mt-5" v-if="notifications.length > 0">
                <div class="col-12">
                    <h2>Notifications</h2>
                </div>

                <div class="col-sm-6 col-lg-4 col-xl-3 overview-card" v-for="notification in notifications" :key="notification.created">
                    <div class="card horizontal h-100">
                        <div class="header w-30 flex-fixed bg-highlight2" style="background-color: #FCD02C">
                            <div class="background-icon">
                                <icon icon="envelope"></icon>
                            </div>
                        </div>
                        <div class="content">
                            <div class="h3">{{notification.title}}</div>
                            <p>{{notification.summary}}</p>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <!--        <div>-->
        <!--            <expression v-model="expression" style="display: inline-block"></expression>-->
        <!--        </div>-->

        <!--        {{expression}}-->
    </div>
</template>

<script>
    import axios from "axios"

    import Dashboard from "./Dashboard.vue"
    import Expression from "@/components/expression/Expression.vue"

    export default {
        name: 'overview',
        components: {Expression, Dashboard},
        data() {
            return {
                "expression": {
                    "type": "Or",
                    "class": "logical",
                    "inputs": [{
                        "type": "And",
                        "class": "logical",
                        "inputs": [{"type": "ConstValue", "class": "literal", "value": true}, {
                            "type": "Equals",
                            "class": "binary",
                            "left_expression": null,
                            "right_expression": {"type": "ConstValue", "class": "literal", "value": 50}
                        }]
                    }, {
                        "type": "ChannelValue",
                        "class": "literal",
                        "thing_id": "thing:bridge:wifiled:1f728c38-b9c2-4e18-b54e-f1a8c5290bff:6001948C9297",
                        "channel_name": "power"
                    }]
                },
                "dashboards": [],
                "notifications": [],
            }
        },
        methods: {
            async removeDashboard(dashboard) {
                await axios.delete(`/plugins/dashboard/api/${dashboard}`)

                this.dashboards.splice(this.dashboards.indexOf(dashboard), 1)
            },
            async addDashboard() {
                const result = await axios.post("/plugins/dashboard/api", {"name": "TODO!"})
                this.dashboards.push(result.data)
            }
        },
        async mounted() {
            let result = await axios.get("/plugins/dashboard/api")
            this.dashboards = result.data

            result = await axios.get("/api/notifications")
            this.notifications = result.data
        }
    }
</script>

<style lang="scss">

</style>
