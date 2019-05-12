<template>
    <div class="script-rule row">
        <div class="col-lg-12" v-if="rule">
            <div class="card">
                <div class="content">
                    <h2><editable-text :value="rule.name" :placeholder="rule.id" @input="updateName($event)"></editable-text></h2>
                </div>

                <div class="header">
                    <span class="h3">When</span>
                </div>
                <div class="content">
                    <div :class="{'text-center': !rule.condition}">
                        <p v-if="!rule.condition">
                            <em>Manual triggered</em><br>
                            <strong>or</strong>
                        </p>

                        <expression v-model="rule.condition" @delete="rule.condition = null" style="display: inline-block"></expression>
                    </div>
                    <div>
                        <button @click="checkCondition()">
                            <icon icon="sync" :spin="conditionCheckRunning" class="cursor-pointer" fixed-width></icon>
                            Evaluate now
                        </button>
                        <span v-if="conditionState != null">
                            Evaluation State:
                            <span v-if="conditionState"><icon icon="check" class="color-okay" fixed-width></icon></span>
                            <span v-else><icon icon="times" class="color-bad" fixed-width></icon></span>
                        </span>
                    </div>
                </div>

                <div class="header">
                    <span class="h3">Then</span>
                </div>
                <div class="content">
                    <div class="row">
                        <div class="col-xl-9">
                            <codemirror v-model="rule.script" :options="{mode: 'text/x-python', lineNumbers: true}"></codemirror>
                        </div>
                        <div class="col-xl-3">
                            <ul>
                                <li>
                                    <code>set</code>(<em>thing_id</em>, <em>channel</em>, <em>value</em>)
                                    <p>
                                        Set Things channel value
                                    </p>
                                </li>
                                <li>
                                    <code>value</code>(<em>thing_id</em>, <em>channel</em>): <em>value</em>
                                    <p>
                                        Get value of given things channel
                                    </p>
                                </li>
                                <li>
                                    <code>call</code>(<em>rule_id</em>)
                                    <p>
                                        Execute rule by Rule Id
                                    </p>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <button @click="execute()">
                        <icon icon="play" fixed-width></icon>
                        Execute now
                    </button>
                    <button @click="save()" class="primary">Save</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios"

    import EditableText from "@/components/EditableText.vue"
    import Expression from "@/components/expression/Expression.vue"
    import { codemirror } from 'vue-codemirror'
    import 'codemirror/lib/codemirror.css'
    import 'codemirror/mode/python/python.js'

    import {Toast} from "@/utils.js"

    export default {
        name: "ScriptRule",
        components: {EditableText, Expression, codemirror},
        props: {
            ruleId: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                rule: null,
                conditionState: null,
                conditionCheckRunning: false
            }
        },
        methods: {
            async getRule() {
                const result = await axios.get(`/api/rules/${this.ruleId}`)

                return result.data
            },
            async updateName(name) {
                await axios.patch(`/api/rules/${this.ruleId}`, {name: name})
                this.rule = await this.getRule()
            },
            async save() {
                await axios.patch(`/api/rules/${this.ruleId}`, {condition: this.rule.condition, script: this.rule.script})
                this.rule = await this.getRule()

                Toast("Rule saved")
            },
            async checkCondition() {
                this.conditionCheckRunning = true
                const result = await axios.get(`/api/rules/${this.ruleId}/condition`)
                this.conditionState = result.data
                this.conditionCheckRunning = false
            },
            async execute() {
                await axios.get(`/api/rules/${this.ruleId}/execute`)
                Toast("Executed Rule")
            }
        },
        async mounted() {
            this.rule = await this.getRule()
        }
    }
</script>

<style lang="scss">
    .script-rule {
    }
</style>
