<template>
    <div class="bridge-settings-form" v-if="bridge">
        <json-schema-form v-model="settings" :schema="bridge.settingsSchema"></json-schema-form>
        <button @click="saveSettings(settings)">Save</button>
    </div>
</template>

<script>
    import axios from "axios"

    import JsonSchemaForm from "@/components/JsonSchema/JsonSchemaForm.vue"

    export default {
        name: 'BridgeSettingsForm',
        components: {JsonSchemaForm},
        props: {
            bridgeId: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                bridge: null,
                settings: null
            }
        },
        methods: {
            async getBridge() {
                const result = await axios.get(`/api/bridges/${this.bridgeId}`)

                return result.data
            },
            async saveSettings(settings) {
                await axios.put(`/api/bridges/${this.bridgeId}/settings`, settings)
            }
        },
        async mounted() {
            this.bridge = await this.getBridge()
            this.settings = this.bridge.settings
        },
    }
</script>

<style lang="scss">

</style>
