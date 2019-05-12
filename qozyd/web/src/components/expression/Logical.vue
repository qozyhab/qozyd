<template>
    <div class="expression logical">
        <draggable class="inputs" v-model="value.inputs" group="inputs" draggable=".input">
            <expression class="input" v-for="(expression, index) in value.inputs" v-model="value.inputs[index]"
                        @delete="deleteInput(index)"></expression>

            <div slot="footer">
                <div @click="showAddExpression = true" class="add">+</div>

                <modal v-if="showAddExpression" @close="showAddExpression = false" :show-buttons="false">
                    <expression-wizard ref="expressionWizard" @finish="value.inputs.push($event), showAddExpression = false"></expression-wizard>
                </modal>
            </div>
        </draggable>

        <div class="type">
            <div class="card h-100">
                <div class="content">
                    <select v-model="value.type">
                        <option value="And">And</option>
                        <option value="Or">Or</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import draggable from 'vuedraggable'

    import Modal from "@/components/Modal.vue"
    import ExpressionWizard from "@/components/forms/Expression/ExpressionWizard.vue"


    export default {
        name: "Logical",
        components: {
            Expression: () => import("./Expression.vue"),
            Modal,
            ExpressionWizard,
            draggable,
        },
        props: ["value"],
        data() {
            return {
                showAddExpression: false
            }
        },
        computed: {},
        methods: {
            deleteInput(index) {
                this.value.inputs.splice(index, 1)
            },
            append() {
                this.value.inputs.push(
                    {
                        "type": "Or",
                        "class": "logical",
                        "inputs": []
                    }
                )
            }
        }
    }
</script>

<style lang="scss">
    $connection-gap: 20px;
    $connection-bias: -10px;
    $stroke-width: 1px;
    $stroke-radius: 15px;
    $stroke-radius-height: 15px;

    .expression.logical {
        > .inputs {
            min-width: 150px;

            > .input {
                position: relative;

                &::after {
                    display: block;
                    content: "";
                    position: absolute;
                    z-index: 1;

                    width: $connection-gap;
                    height: 0;
                    border-bottom: $stroke-width solid #333;

                    right: -$connection-gap - $connection-bias;
                    top: calc(50% - #{$stroke-width / 2});
                }

            }
        }
    }
</style>
