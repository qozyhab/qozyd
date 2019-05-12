<template>
    <modal v-if="show" :show-buttons="false">
        <h1>{{title}}</h1>
        <p>
            {{message}}
        </p>
        <button @click="accept()">Yes</button>
        <button @click="decline()">No</button>
    </modal>
</template>

<script>
    import Modal from "./Modal.vue"

    export default {
        name: "confirm",
        components: {Modal},
        data() {
            return {
                show: false,
                title: "",
                message: "",
                resolve: null,
                reject: null,
            }
        },
        methods: {
            open(title, message) {
                this.title = title
                this.message = message

                this.show = true

                return new Promise((resolve, reject) => {
                    this.resolve = resolve
                    this.reject = reject
                })
            },
            accept() {
                this.resolve(true)
                this.show = false
            },
            decline() {
                this.resolve(false)
                this.show = false
            }
        }
    }
</script>

<style lang="scss">

</style>
