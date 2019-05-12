export default {
    props: ["value"],
    data() {
        return {
            settings: this.value || {}
        }
    },
    methods: {
        validate() {
            return true
        }
    },
    watch: {
        settings: {
            deep: true,
            handler: function (value) {
                this.$emit("input", value)
            }
        }
    }
}
