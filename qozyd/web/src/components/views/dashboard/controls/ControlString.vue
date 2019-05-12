<template>
    <div class="control-string">
        {{value}}
    </div>
</template>

<script>
    import BaseControl from "./BaseControl.js"

    export default {
        name: "ControlString",
        mixins: [BaseControl],
        data() {
            return {
                value: null,
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
    .control-string {
        text-align: center;
    }
</style>
