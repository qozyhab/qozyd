<template>
    <div class="row">
        <div class="col-lg-4">
            <div class="card" @click="select('logical', 'And')">
                <div class="content">And</div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="card" @click="select('logical', 'Or')">
                <div class="content">Or</div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="card" @click="select('binary', 'Comparison')">
                <div class="content">Comparison</div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="card" @click="select('literal', 'ConstValue')">
                <div class="content">Constant Value</div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="card" @click="select('literal', 'ChannelValue')">
                <div class="content">Things Channel Value</div>
            </div>
        </div>
    </div>
</template>

<script>
    const expressionTypeMap = {
        logical: {
            And: {group: "logical", type: "And", inputs: []},
            Or: {group: "logical", type: "Or", inputs: []}
        },
        binary: {
            Comparison: {group: "binary", type: "Equals", inputs: [null, null]}
        },
        literal: {
            ConstValue: {group: "literal", type: "ConstValue"},
            ChannelValue: {group: "literal", type: "ChannelValue"}
        }
    }

    export default {
        name: "ExpressionWizard",
        data() {
            return {
                expressionTypeMap
            }
        },
        methods: {
            select(group, type) {
                this.$emit("finish", expressionTypeMap[group][type])
            }
        }
    };
</script>

<style lang="scss">
</style>
