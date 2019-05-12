<template>
    <div class="bridge-settings-json" v-if="bridge">
        <textarea v-model="settingsJson" spellcheck="false"></textarea>
        <button @click="saveSettings(JSON.parse(settingsJson))" class="primary">Save</button>
    </div>
</template>

<script>
    import axios from "axios"

    import JsonSchemaForm from "@/components/JsonSchema/JsonSchemaForm.vue"

    export default {
        name: 'BridgeSettingsJson',
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
                settingsJson: null
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
            this.settingsJson = JSON.stringify(this.bridge.settings, null, 4)
        },
    }
</script>

<style lang="scss">
    .bridge-settings-json {
        textarea {
            resize: none;
            height: 800px;
        }
    }
</style>
