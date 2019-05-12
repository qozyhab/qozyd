<template>
    <div class="control">
        <ul class="menu">
            <li v-if="editMode">
                <a @click="showSettingsModal = true">
                    <icon icon="cogs"></icon>
                </a>
            </li>
        </ul>

        <h2 class="title">{{control.headline}}</h2>

        <component :is="controlComponent" :settings="control.settings"></component>

        <modal v-if="showSettingsModal" @close="showSettingsModal = false">
            <control-settings v-model="control"></control-settings>
        </modal>
    </div>
</template>

<script>
    import Modal from "@/components/Modal.vue";
    import ControlSettings from "@/components/forms/ControlSettings/ControlSettings.vue";

    import ControlString from "./ControlString.vue"
    import ControlGraph from "./ControlGraph"
    import ControlNumber from "./ControlNumber.vue"
    import ControlSwitch from "./ControlSwitch.vue"
    import ControlColor from "./ControlColor.vue"
    import ControlDimmer from "./ControlDimmer.vue"

    import {mapState} from 'vuex'


    const controls = {
        String: ControlString,
        Graph: ControlGraph,
        Number: ControlNumber,
        Switch: ControlSwitch,
        Color: ControlColor,
        Dimmer: ControlDimmer,
    };

    export default {
        name: "control",
        components: {Modal, ControlSettings},
        props: {
            control: {
                required: true
            },
        },
        data() {
            return {
                showSettingsModal: false
            }
        },
        computed: {
            controlComponent() {
                return controls[this.control.type];
            },
            ...mapState('dashboard', [
                'editMode'
            ])
        },
    };
</script>

<style lang="scss">
    .control {
        > .title {
            font-size: 0.8rem;
            text-transform: uppercase;
            color: #ccc;
        }
    }
</style>
