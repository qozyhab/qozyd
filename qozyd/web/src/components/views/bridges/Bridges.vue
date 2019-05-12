<template>
    <div class="bridges row">
            <div class="col-lg-2">
                <div class="card">
                    <nav>
                        <ul class="menu vertical">
                            <li v-for="bridgeType in bridgeTypes" :key="bridgeType" @click="addBridge(bridgeType)">
                                <icon icon="plus-circle"></icon>

                                {{bridgeType}}
                            </li>
                            <li>Install new</li>
                        </ul>
                    </nav>
                </div>
            </div>
            <div class="col-lg-10">
                <div class="row">
                    <div class="col-12">
                        <transition-group name="fade" tag="div">
                            <bridge v-for="bridge in bridges" :key="bridge" :bridge-id="bridge" class="mb-2" @remove="removeBridge(bridge)"></bridge>
                        </transition-group>
                    </div>
                </div>
            </div>
    </div>
</template>

<script>
    import axios from "axios"
    import Bridge from "./Bridge.vue"

    export default {
        name: 'bridges',
        components: {Bridge},
        data() {
            return {
                bridgeTypes: [],
                bridges: []
            }
        },
        methods: {
            async getBridges() {
                const result = await axios.get("/api/bridges")

                return result.data
            },
            async addBridge(bridgeType) {
                await axios.post("/api/bridges", JSON.stringify(bridgeType))

                this.bridges = await this.getBridges()
            },
            async removeBridge(bridgeId) {
                await axios.delete(`/api/bridges/${bridgeId}`)

                this.bridges = await this.getBridges()
            }
        },
        async mounted() {
            this.bridges = await this.getBridges()

            const result = await axios.get("/api/bridges/types")
            this.bridgeTypes = result.data
        }
    }
</script>

<style lang="scss">

</style>
