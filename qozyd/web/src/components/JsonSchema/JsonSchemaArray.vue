<template>
    <div>
        <transition-group name="fade" tag="ul" class="list-group">
            <li v-for="(subValue, index) in myValue" :key="index">
                <i style="float: right;" @click="myValue.splice(index, 1)">
                    <icon icon="trash"></icon>
                </i>
                <json-schema-form v-model="myValue[index]" :schema="schema.items"></json-schema-form>
            </li>
        </transition-group>

        <a @click="myValue.push(null)">
            <icon icon="plus-square"></icon>
        </a>
    </div>
</template>

<script>
    export default {
        name: "JsonSchemaArray",
        components: {
            JsonSchemaForm: () => import('./JsonSchemaForm.vue')
        },
        props: {
            value: {
                required: false
            },
            schema: {
                required: true
            }
        },
        data() {
            return {
                myValue: this.value || this.getDefaultValue()
            }
        },
        methods: {
            getDefaultValue() {
                return []
            },
            init() {
                this.myValue = this.value || this.getDefaultValue()
                this.$emit("input", this.myValue)
            }
        },
        watch: {
            schema: function () {
                this.init()
            },
            myValue: {
                handler(newValue) {
                    this.$emit("input", newValue);
                },
                deep: true
            }
        },
        created() {
            this.init()
        }
    };
</script>

<style lang="scss">
</style>
