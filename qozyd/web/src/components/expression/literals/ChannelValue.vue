<template>
    <div class="expression">
        <div class="type">
            <div class="card horizontal h-100">
                <div class="header bg-highlight-2"></div>
                <div class="content">
                    <div>
                        <channel-value-watcher v-if="value.thing_id && value.channel_name" :thing-id="value.thing_id" :channel="value.channel_name"></channel-value-watcher>
                    </div>
                    <div>
                        <icon @click="settings = true" icon="cogs"></icon>
                        <small>{{value.thing_id}} {{value.channel_name}}</small>

                        <modal v-if="settings" @close="settings = false">
                            <channel-select v-model="channel"></channel-select>
                        </modal>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import ChannelValue from "@/components/ChannelValue.vue"
    import Modal from "@/components/Modal.vue"
    import ChannelSelect from "@/components/ChannelSelect.vue"

    export default {
        name: "ChannelValue",
        components: {ChannelValueWatcher: ChannelValue, Modal, ChannelSelect},
        props: ["value"],
        data() {
            return {
                settings: false,
                channel: [this.value.thing_id, this.value.channel_name]
            }
        },

        watch: {
            channel(value) {
                this.value.thing_id = value[0]
                this.value.channel_name = value[1]
            }
        }
    }
</script>

<style lang="scss">
</style>
