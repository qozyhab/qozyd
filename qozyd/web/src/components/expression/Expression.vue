<template>
    <div class="expression-container" @mouseover.stop="hover = true" @mouseout="hover = false" :class="{'hover': hover}">
        <ul class="settings" v-if="value">
            <li @click="$emit('delete')"><icon icon="trash"></icon></li>
            <li @click="showSurroundExpression = true"><icon icon="arrow-right"></icon></li>
        </ul>

        <modal v-if="showSurroundExpression" @close="showSurroundExpression = false" :show-buttons="false">
            <expression-wizard ref="expressionWizard" @finish="surround($event), showSurroundExpression = false"></expression-wizard>
        </modal>

        <component v-if="value" class="component" :is="expressionComponent" :value="value" @input="$emit('input', $event)"></component>

        <div v-else class="add">
            <span @click="showAddExpression = true"><icon icon="plus-circle" fixed-width></icon> Add Expression</span>
        </div>

        <modal v-if="showAddExpression" @close="showAddExpression = false" :show-buttons="false">
            <expression-wizard ref="expressionWizard" @finish="$emit('input', $event), showAddExpression = false"></expression-wizard>
        </modal>
    </div>
</template>

<script>
    import Literal from "./Literal.vue"
    import Binary from "./Binary.vue"
    import Logical from "./Logical.vue"

    import Modal from "@/components/Modal.vue"
    import ExpressionWizard from "@/components/forms/Expression/ExpressionWizard.vue"

    const groups = {
        literal: Literal,
        binary: Binary,
        logical: Logical,
    };

    export default {
        name: "Expression",
        components: {Modal, ExpressionWizard},
        props: ["value"],
        data() {
            return {
                showAddExpression: false,
                showSurroundExpression: false,
                hover: false
            }
        },
        computed: {
            expressionComponent() {
                return groups[this.value.group];
            },
        },
        methods: {
            surround(expression) {
                expression.inputs[0] = this.value

                this.$emit("input", expression)
            }
        }
    }
</script>

<style lang="scss">
    .expression-container {
        position: relative;
        border: 1px solid transparent;
        transition: all ease-in-out 300ms;
        background-color: #fff;

        > ul.settings {
            position: absolute;
            right: -1px;
            top: -1.5rem;
            list-style: none;
            display: none;

            height: 1.5rem;

            padding: 0;
            margin: 0;

            opacity: 0;

            transition: all ease-in-out 300ms;
            background-color: #fff;

            border-left: 1px solid #e4e4e4;
            border-top: 1px solid #e4e4e4;
            border-right: 1px solid #e4e4e4;


            > li {
                display: inline-block;
                line-height: 1.5rem;
                margin: 0 10px;
            }
        }

        &.hover {
            border: 1px solid #e4e4e4;
            box-shadow: 0 2px 2px 0 rgba(0,0,0,0.14), 0 3px 1px -2px rgba(0,0,0,0.12), 0 1px 5px 0 rgba(0,0,0,0.2);
            //transform: scale(1.03);
            z-index: 10;


            > ul.settings {
                opacity: 1;
                display: block;
            }
        }

        > .expression {
            display: flex;
            flex-direction: row;
            align-items: stretch;
            justify-content: flex-end;
            padding: 10px 0;
        }

        > .add {
            padding: 10px;
            border: 2px dashed #000;
            text-align: center;
        }

        > .component {
            > .type {
                min-height: 60px;
                min-width: 150px;

                margin: 10px;
            }

            .add {
                border: 1px dashed green;
                margin: 10px;
                text-align: center;
                width: 150px;
                margin-left: auto;
            }
        }
    }


</style>
