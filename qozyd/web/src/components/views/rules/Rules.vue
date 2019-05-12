<template>
    <div class="rules row">
        <div class="col-lg-2">
            <div class="card">
                <nav>
                    <ul class="menu vertical">
                        <li v-popper:bottom="'add-types'" class="relative">
                            <icon icon="plus-circle" fixed-width></icon> Add rule

                            <div ref="add-types" class="dropdown w-100">
                                <ul class="menu vertical">
                                    <li @click="createScriptRule()"><icon icon="code" fixed-width></icon> Script</li>
                                </ul>
                            </div>
                        </li>
                    </ul>
                </nav>
            </div>
        </div>
        <div class="col-lg-10">
            <div class="row">
                <div class="col-12">
                    <transition-group name="fade" tag="div">
                        <rule v-for="rule in rules" :key="rule" :rule-id="rule" class="mb-2" @remove="removeRule(rule)"></rule>
                    </transition-group>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios"

    import Rule from "./Rule.vue"

    export default {
        name: "Rules",
        components: {Rule},
        data() {
            return {
                rules: [],
            }
        },
        methods: {
            async getRules() {
                const result = await axios.get("/api/rules")

                return result.data
            },
            async createScriptRule() {
                await axios.post("/api/rules/script")
                this.rules = await this.getRules()
            },
            async removeRule(ruleId) {
                await axios.delete(`/api/rules/${ruleId}`)

                this.rules = await this.getRules()
            }
        },
        async mounted() {
            this.rules = await this.getRules()
        }
    }
</script>

<style lang="scss">

</style>
