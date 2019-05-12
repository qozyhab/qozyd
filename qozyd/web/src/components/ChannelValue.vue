<template>
    <span>{{value}}</span>
</template>

<script>
    import ChannelSubscriber from "@/ChannelSubscriber.js"

    export default {
        name: "ChannelValue",
        props: {
            thingId: {
                type: String,
                required: true
            },
            channel: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                subscription: null,
                value: null
            }
        },
        methods: {
            async subscribe() {
                if (this.subscription) {
                    this.subscription.unsubscribe()
                }

                this.subscription = await ChannelSubscriber.subscribe(this.thingId, this.channel, (update) => {
                    this.value = update.value
                })
            }
        },
        watch: {
            async thingId() {
                await this.subscribe()
            },
            async channel() {
                await this.subscribe()
            }
        },
        async mounted() {
            await this.subscribe()
        },
        destroyed() {
            if (this.subscription) {
                this.subscription.unsubscribe()
            }
        }
    }
</script>

<style lang="scss">

</style>
