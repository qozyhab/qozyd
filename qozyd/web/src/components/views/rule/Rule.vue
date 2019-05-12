<template>
    <div>
        <component v-if="ruleComponent" :is="ruleComponent" :rule-id="ruleId"></component>
    </div>
</template>

<script>
    import axios from "axios"

    import ScriptRule from "./ScriptRule.vue";

    const ruleComponents = {
        "ScriptRule": ScriptRule,
    }

    export default {
        name: "Rule",
        props: {
            ruleId: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                rule: null,
            }
        },
        computed: {
            ruleComponent() {
                if (this.rule && this.rule.type in ruleComponents) {
                    return ruleComponents[this.rule.type]
                }

                return null
            }
        },
        methods: {
            async getRule() {
                const result = await axios.get(`/api/rules/${this.ruleId}`)

                return result.data
            }
        },
        async mounted() {
            this.rule = await this.getRule()
        }
    }
</script>

<style lang="scss">

</style>
