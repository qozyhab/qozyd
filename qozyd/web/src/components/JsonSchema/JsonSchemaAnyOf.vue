<template>
    <div>
        <div>
            <select v-model="subschemaIndex">
                <option v-for="(subSchema, index) in schema.anyOf" :value="index">{{subSchema.title}}</option>
            </select>

            <json-schema-form v-if="subschemaIndex != null" v-model="myValue" :schema="schema.anyOf[subschemaIndex]"></json-schema-form>
        </div>

        <small v-if="schema.description">
            {{schema.description}}
        </small>
    </div>
</template>

<script>
    import Ajv from "ajv"

    const ajv = new Ajv()

    export default {
        name: "JsonSchemaAnyOf",
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
                myValue: this.value,
                defaultValue: this.value,
                defaultSubschemaIndex: this.getMatchingSchemaIndex(this.schema, this.value),
                subschemaIndex: this.getMatchingSchemaIndex(this.schema, this.value),
            }
        },
        methods: {
            init() {
                this.myValue = this.value
                this.defaultValue = this.value
                this.defaultSubschemaIndex = this.getMatchingSchemaIndex(this.schema, this.value)
                this.subschemaIndex = this.getMatchingSchemaIndex(this.schema, this.value)

                this.$emit("input", this.myValue)
            },
            getMatchingSchemaIndex(anyOfSchemas, value) {
                let result = null

                anyOfSchemas["anyOf"].forEach((schema, index) => {
                    if (ajv.validate(schema, value)) {
                        result = index
                        return false
                    }
                })

                return result
            }
        },
        watch: {
            subschemaIndex: function (value) {
                if (value !== this.defaultSubschemaIndex) {
                    this.myValue = null
                } else {
                    this.myValue = this.defaultValue
                }
            },
            myValue: {
                handler(newValue) {
                    this.$emit("input", newValue)
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
