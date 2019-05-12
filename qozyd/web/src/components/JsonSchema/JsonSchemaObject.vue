<template>
    <div>
        <div v-for="(subSchema, field) in schema.properties" :key="field">
            <label>{{subSchema.title || field}}:</label>
            <json-schema-form v-model="myValue[field]" :schema="subSchema"></json-schema-form>
        </div>
    </div>
</template>

<script>
    export default {
        name: "JsonSchemaObject",
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
                let defaultValue = {};

                /*
                 * Fill const values
                 */
                for (let propertyName in this.schema.properties) {
                    const property = this.schema.properties[propertyName]

                    if (property.const) {
                        defaultValue[propertyName] = property.const
                    }
                }

                return defaultValue
            },
            init() {
                this.myValue = this.value || this.getDefaultValue()
                this.$emit("input", this.myValue)
            }
        },
        watch: {
            schema() {
                this.init()
            },
            value() {
                this.init()
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
