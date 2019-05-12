<template>
    <div class="channel-select row">
        <div class="col-lg-6">
            <label>
                Thing
                <thing-select v-model="thing" :filter="thingFilter" ref="thingSelect"></thing-select>
            </label>
        </div>

        <div class="col-lg-6">
            Channel
            <ul class="list-group" v-if="thing">
                <li class="list-item" v-for="channel in channels" :key="channel.id" @click="$emit('input', [thing, channel.name])" :class="{ active: value && value[1] == channel.name }">
                    {{channel.name}}
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import axios from "axios"
    import ThingSelect from "./ThingSelect.vue"

    export default {
        name: "ChannelSelect",
        props: ["value", "filter"],
        components: {ThingSelect},
        data() {
            return {
                thing: this.value != null ? this.value[0] : null,
                channels: []
            }
        },
        methods: {
            thingFilter(thing) {
                // Filter out all things, where the available channel count for the given channel filter equals to 0
                const thingChannels = Object.values(thing.channels)
                const filteredChannels = this.doFilter(thingChannels)

                return filteredChannels.length > 0
            },
            async getThing(thingId) {
                let result = await axios.get(`/api/things/${thingId}`)

                return result.data
            },
            doFilter(channels) {
                if (this.filter) {
                    return channels.filter(this.filter)
                }

                return channels
            }
        },
        watch: {
            thing: {
                handler: async function (value) {
                    if (value) {
                        //this.$emit('input', null)
                        const thing = await this.getThing(value)
                        this.channels = this.doFilter(Object.values(thing.channels))
                    } else {
                        this.channels = []
                    }
                },
                immediate: true
            }
        }
    }
</script>

<style lang="scss">
</style>
