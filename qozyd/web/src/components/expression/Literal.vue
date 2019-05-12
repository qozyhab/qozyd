<template>
    <component :is="componentType" v-model="value"></component>
</template>

<script>
    import ConstValue from "./literals/ConstValue.vue";
    import ChannelValue from "./literals/ChannelValue.vue";

    const literalTypeComponents = {
        "ConstValue": ConstValue,
        "ChannelValue": ChannelValue
    }

    export default {
        name: "Literal",
        props: ["value"],
        computed: {
            componentType() {
                return literalTypeComponents[this.value.type]
            }
        }
    }
</script>

<style lang="scss">
</style>
