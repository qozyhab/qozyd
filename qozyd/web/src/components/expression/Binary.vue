<template>
    <div class="expression binary">
        <modal v-if="showAddLeftExpression" @close="showAddLeftExpression = false" :show-buttons="false">
            <expression-wizard @finish="leftExpression = $event, showAddLeftExpression = false"></expression-wizard>
        </modal>
        <expression v-if="value.inputs[0]" v-model="value.inputs[0]"
                    @delete="leftExpression = null"></expression>
        <div v-else class="add" @click="showAddLeftExpression = true">Add</div>


        <div class="type">
            <div class="card h-100">
                <div class="content">
                    <select v-model="value.type">
                        <option value="Equals">=</option>
                        <option value="NotEquals">!=</option>
                        <option value="GreaterThan">&gt;</option>
                        <option value="GreaterThanOrEquals">&gt;=</option>
                        <option value="LowerThan">&lt;</option>
                        <option value="LowerThanOrEquals">&lt;=</option>
                    </select>
                </div>
            </div>
        </div>


        <modal v-if="showAddRightExpression" @close="showAddRightExpression = false" :show-buttons="false">
            <expression-wizard @finish="rightExpression = $event, showAddRightExpression = false"></expression-wizard>
        </modal>
        <expression v-if="value.inputs[1]" v-model="value.inputs[1]"
                    @delete="rightExpression = null"></expression>
        <div v-else class="add" @click="showAddRightExpression = true">Add</div>
    </div>
</template>

<script>
    import Modal from "@/components/Modal.vue"
    import ExpressionWizard from "@/components/forms/Expression/ExpressionWizard.vue"


    export default {
        name: "Binary",
        components: {
            Expression: () => import("./Expression.vue"),
            Modal,
            ExpressionWizard
        },
        props: ["value"],
        data() {
            return {
                showAddRightExpression: false,
                showAddLeftExpression: false,
            }
        },
        computed: {
            leftExpression: {
                get() {
                    return this.value.inputs[0]
                },
                set(value) {
                    this.value.inputs[0] = value
                    this.$forceUpdate()
                }
            },
            rightExpression: {
                get() {
                    return this.value.inputs[1]
                },
                set(value) {
                    this.value.inputs[1] = value
                    this.$forceUpdate()
                }
            }
        }
    }
</script>

<style lang="scss">
    .expression.binary {
    }
</style>
