<template>
    <div class="control-number">
        <span class="value">{{ format(value) }}</span>
    </div>
</template>

<script>
    import BaseControl from "./BaseControl.js"
    import ssf from "ssf"

    export default {
        name: "ControlNumber",
        mixins: [BaseControl],
        data() {
            return {
                value: null
            }
        },
        methods: {
            format(value) {
                if (this.settings.format) {
                    return ssf.format(this.settings.format, value)
                }

                return value
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
    .control-number {
        text-align: center;
    }
</style>
