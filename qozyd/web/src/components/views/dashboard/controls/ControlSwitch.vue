<template>
    <div class="channel-switch">
        <label>
            <input type="checkbox" @input="setValue(!activated)" :value="activated"/>
            <div>
                <icon icon="power-off" size="lg"></icon>

                <svg class="indicator cover-parent" viewBox="0 0 100 100">
                    <use class="indicator-icon" :class="{'on': activated}" xlink:href="#spinning-border"></use>
                </svg>

                <svg class="loading cover-parent" viewBox="0 0 100 100" v-if="loading">
                    <use class="loading-icon" xlink:href="#spinning-border"></use>
                </svg>
            </div>
        </label>
    </div>
</template>

<script>
    import BaseControl from "./BaseControl.js"


    export default {
        name: "ControlSwitch",
        mixins: [BaseControl],
        data() {
            return {
                activated: null,
                loading: false
            }
        },
        methods: {
            async setValue(activated) {
                this.loading = true
                this.$forceUpdate()

                await this.applyChannel(this.settings.channel, activated)

                this.loading = false
            }
        },
        async mounted() {
            const self = this

            await this.autoWatchChannel("settings.channel", (data) => {
                self.activated = data.value
            })
        }
    };
</script>

<style lang="scss">
    .channel-switch {
        text-align: center;

        label {
            display: inline-block;

            > div {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background-color: #37474f;
                color: #f5f5f5;

                position: relative;

                .indicator {
                    pointer-events: none;
                    overflow: visible;

                    > .indicator-icon {
                        color: #00838f;
                        stroke-width: 4;
                        stroke-dashoffset: 314.2033996582031;
                        transition: stroke-dashoffset 0.5s ease-in;

                        &.on {
                            stroke-dashoffset: 0;
                            transition: stroke-dashoffset 0.5s ease-in;
                        }
                    }
                }

                .loading {
                    overflow: visible;

                    > .loading-icon {
                        stroke-width: 4;
                        color: #ff00ff;
                        stroke-dashoffset: 628.406799316;
                        animation: rotate 2s linear infinite;

                        @keyframes rotate {
                            to {
                                stroke-dashoffset: 0;
                            }
                        }
                    }
                }
            }

            > input {
                display: none;

                &:checked + div {
                    border-color: green;
                }
            }
        }
    }
</style>
