<template>
    <div class="expression">
        <div class="type">
            <div class="card h-100">
                <div class="content">
                    <icon @click="settings = true" icon="cogs"></icon>
                    <em>"{{ value.value }}"</em>

                    <modal v-if="settings" @close="settings = false">
                        <div class="input-group">
                            <select class="appendix" v-model="type">
                                <option value="number">Number</option>
                                <option value="string">Text</option>
                            </select>
                            <input v-if="type == 'number'" type="number" v-model.number="value.value"/>
                            <input v-if="type == 'string'" type="text" v-model="value.value"/>
                        </div>
                    </modal>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Modal from "@/components/Modal.vue"

    export default {
        name: "ConstValue",
        components: {Modal},
        props: ["value"],
        data() {
            return {
                type: null,
                settings: false
            }
        },
        watch: {
            value: {
                handler: function(value) {
                    if (value) {
                        switch (typeof value.value) {
                            case "number":
                                this.type = "number"
                                return
                            case "string":
                                this.type = "string"
                                return
                        }
                    }

                    this.type = "number"
                },
                immediate: true
            },
            type: function (value) {
                if (value === "number") {
                    const val = parseFloat(this.value.value)

                    if (!isNaN(val)) {
                        this.value.value = val
                    } else {
                        this.value.value = null
                    }
                } else {
                    this.value.value = "" + this.value.value
                }
            }
        }
    }
</script>

<style lang="scss">
</style>
