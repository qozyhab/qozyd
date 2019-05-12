<template>
    <div class="item-dimmer">
        <input type="range" :value="value" @change="applyChannel(settings.channel, $event.target.value)" min="0"
               max="100"/>
    </div>
</template>

<script>
    import BaseControl from "./BaseControl.js"


    export default {
        name: "ControlDimmer",
        mixins: [BaseControl],
        data() {
            return {
                value: null
            }
        },
        async mounted() {
            const self = this

            await this.autoWatchChannel("settings.channel", (data) => {
                self.value = data.value
            })
        }
    };
</script>

<style lang="scss">
    .channel-dimmer {

    }
</style>
