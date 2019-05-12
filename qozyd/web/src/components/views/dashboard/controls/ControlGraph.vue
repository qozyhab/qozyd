<template>
    <div class="item-string">
        <graph class="graph" :columns="graphColumns(data)" :type="settings.type" :x-axis="true" :y-min="settings.yMin"
               :y-max="settings.yMax"></graph>
    </div>
</template>

<script>
    import Graph from "@/components/Graph.vue";
    import BaseControl from "./BaseControl.js"

    export default {
        name: "ControlGraph",
        mixins: [BaseControl],
        components: {Graph},
        data() {
            return {
                itemData: {},
                data: null
            }
        },
        methods: {
            graphColumns(channel) {
                if (channel) {
                    let result = []

                    Object.values(this.channelData).forEach(() => {
                        const history = ["history"]
                            .concat(this.data.history.map(d => d.value))
                            .concat([this.data.value])

                        result.push(history)
                    })

                    return result
                }

                return [["history"]]
            }
        },
        async mounted() {
            this.settings.channels.forEach(async item => {
                await this.watchChannel(item, data => {
                    this.channelData[item] = data
                    this.data = data
                })
            })
        }
    }
</script>

<style lang="scss">
    .value {

    }
</style>
