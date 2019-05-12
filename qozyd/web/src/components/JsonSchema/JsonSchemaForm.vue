<template>
    <div>
        <select v-if="'enum' in schema" v-model="myValue">
            <option v-for="(option, index) in schema.enum" :key="index" :value="option">{{option}}</option>
        </select>

        <input v-else-if="schema.type == 'string'" type="text" v-model="myValue"/>

        <input v-else-if="schema.type == 'number'" type="text" v-model.number="myValue"/>

        <input v-else-if="schema.type == 'integer'" type="text" v-model.number="myValue"/>

        <input v-else-if="schema.type == 'boolean'" type="checkbox" v-model="myValue"/>

        <json-schema-object v-else-if="schema.type == 'object'" v-model="myValue" :schema="schema"></json-schema-object>

        <json-schema-array v-else-if="schema.type == 'array'" v-model="myValue" :schema="schema"></json-schema-array>

        <json-schema-any-of v-else-if="schema.anyOf" v-model="myValue" :schema="schema"></json-schema-any-of>

        <small v-if="schema.description">
            {{schema.description}}
        </small>

        <ul v-if="!validate(myValue)">
            <li v-for="error in validate.errors">{{error.message}}</li>
        </ul>
    </div>
</template>

<script>
    import Ajv from "ajv"
    import JsonSchemaAnyOf from "./JsonSchemaAnyOf.vue"
    import JsonSchemaObject from "./JsonSchemaObject.vue"
    import JsonSchemaArray from "./JsonSchemaArray.vue"


    const ajv = new Ajv()

    export default {
        name: "JsonSchemaForm",
        components: {JsonSchemaAnyOf, JsonSchemaObject, JsonSchemaArray},
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
                myValue: this.value,
                validate: ajv.compile(this.schema)
            };
        },
        methods: {
            init() {
                this.myValue = this.value
                this.$emit("input", this.myValue)
            }
        },
        watch: {
            myValue: {
                handler(newValue) {
                    this.$emit("input", newValue)
                },
                deep: true
            },
            value(value) {
                this.init()
            }
        },
        created() {
            this.init()
        }
    };
</script>

<style lang="scss">
</style>
