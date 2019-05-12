<template>
    <div class="control-color">
        <div class="color-picker">
            <div>
                <div class="circle" :style="'background-color: ' + hexColor(value)" @click="choose = !choose">
                    {{hexColor(value)}}
                </div>
                <svg class="loading cover-parent" viewBox="0 0 100 100" v-if="loading">
                    <use class="loading-icon" xlink:href="#spinning-border"></use>
                </svg>
            </div>

            <div class="circle small x" :class="{'n': choose}" :style="'background-color: ' + hexColor([0, 255, 0])"
                 @click="applyChannel(settings.channel, {'type': 'rgb', 'value': [0, 255, 0]})"></div>
            <div class="circle small x" :class="{'ne': choose}" :style="'background-color: ' + hexColor([255, 0, 0])"
                 @click="applyChannel(settings.channel, {'type': 'rgb', 'value': [255, 0, 0]})"></div>
            <div class="circle small x" :class="{'e': choose}" :style="'background-color: ' + hexColor([0, 0, 255])"
                 @click="applyChannel(settings.channel, {'type': 'rgb', 'value': [0, 0, 255]})"></div>
            <div class="circle small x" :class="{'se': choose}" :style="'background-color: ' + hexColor([255, 255, 0])"
                 @click="applyChannel(settings.channel, {'type': 'rgb', 'value': [255, 255, 0]})"></div>
            <div class="circle small x" :class="{'s': choose}" :style="'background-color: ' + hexColor([0, 255, 255])"
                 @click="applyChannel(settings.channel, {'type': 'rgb', 'value': [0, 255, 255]})"></div>
            <div class="circle small x" :class="{'sw': choose}" :style="'background-color: ' + hexColor([255, 0, 255])"
                 @click="applyChannel(settings.channel, {'type': 'rgb', 'value': [255, 0, 255]})"></div>
            <div class="circle small x" :class="{'w': choose}" :style="'background-color: ' + hexColor([128, 255, 0])"
                 @click="applyChannel(settings.channel, {'type': 'rgb', 'value': [128, 255, 0]})"></div>
            <div class="circle small x" :class="{'nw': choose}" :style="'background-color: ' + hexColor([0, 255, 128])"
                 @click="applyChannel(settings.channel, {'type': 'rgb', 'value': [0, 255, 128]})"></div>
        </div>
    </div>
</template>

<script>
    import BaseControl from "./BaseControl.js"

    export default {
        name: "ControlColor",
        mixins: [BaseControl],
        data() {
            return {
                choose: false,
                value: null,
                loading: false,
            };
        },
        methods: {
            hexColor: rgb => {
                if (rgb) {
                    return (
                        "#" +
                        rgb[0].toString(16).padStart(2, "0") +
                        rgb[1].toString(16).padStart(2, "0") +
                        rgb[2].toString(16).padStart(2, "0")
                    );
                }

                return "#000000"
            }
        },
        async mounted() {
            const self = this

            await this.autoWatchChannel("settings.channel", (data) => {
                self.value = data.value
            })
        }
    }
</script>

<style lang="scss">
    .control-color {
        text-align: center;

        .color-picker {
            position: relative;
            display: inline-block;

            .circle {
                width: 100px;
                height: 100px;
                border-radius: 50%;
                position: relative;
                z-index: 2;

                display: flex;
                align-items: center;
                justify-content: center;

                z-index: 2;

                &.small {
                    width: 60px;
                    height: 60px;
                }
            }

            .x {
                position: absolute;
                z-index: 1;

                top: 0;
                left: 0;
                right: 0;
                bottom: 0;

                margin: auto auto;

                opacity: 1;

                transition: all 0.3s ease-in-out;
                //transform: translateY(0);
            }

            .n {
                opacity: 1;
                transform-origin: 50% 50%;
                transform: translateY(-100px);
            }

            .ne {
                opacity: 1;
                transform-origin: 50% 50%;
                transform: rotateZ(45deg) translateY(-100px);
            }

            .e {
                opacity: 1;
                transform-origin: 50% 50%;
                transform: rotateZ(90deg) translateY(-100px);
            }

            .se {
                opacity: 1;
                transform-origin: 50% 50%;
                transform: rotateZ(135deg) translateY(-100px);
            }

            .s {
                opacity: 1;
                transform-origin: 50% 50%;
                transform: rotateZ(180deg) translateY(-100px);
            }

            .sw {
                opacity: 1;
                transform-origin: 50% 50%;
                transform: rotateZ(225deg) translateY(-100px);
            }

            .w {
                opacity: 1;
                transform-origin: 50% 50%;
                transform: rotateZ(270deg) translateY(-100px);
            }

            .nw {
                opacity: 1;
                transform-origin: 50% 50%;
                transform: rotateZ(315deg) translateY(-100px);
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
    }
</style>
