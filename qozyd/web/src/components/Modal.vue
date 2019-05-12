<template>
    <transition name="modal">
        <div class="modal-mask" @click.self="$emit('close')">
            <div class="modal">
                <slot></slot>

                <slot name="buttons" v-if="showButtons">
                    <div class="footer text-right mt-3">
                        <button @click="$emit('close')">Close</button>
                        <button class="primary" @click="$emit('close')">OK</button>
                    </div>
                </slot>
            </div>
        </div>
    </transition>
</template>

<script>
    export default {
        name: "modal",
        props: {
            showButtons: {
                default: true,
                type: Boolean
            }
        }
    }
</script>

<style lang="scss">
    .modal-mask {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.4);

        z-index: 10000;

        overflow: visible;

        transition: opacity .3s ease;

        > .modal {
            width: 40%;
            min-height: 100px;

            background-color: #fff;
            color: #000;

            margin: 0 auto;
            margin-top: 10%;

            padding: 20px;

            box-shadow: 0 2px 8px rgba(0, 0, 0, .33);

            transition: transform .3s ease;

            > .footer {
                border-top: 1px solid #e4e4e4;
                padding-top: .5em;
            }
        }
    }
</style>
