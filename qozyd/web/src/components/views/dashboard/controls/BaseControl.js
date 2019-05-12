import axios from "axios"
import ChannelSubscriber from "@/ChannelSubscriber.js"


export default {
    props: {
        settings: {
            required: false,
        }
    },
    methods: {
        async fetchChannel(channel) {
            const [thing, channelName] = channel

            const result = await axios.get(`/api/things/${thing}/channels/${channelName}`)

            return result.data
        },
        async watchChannel(channel, callback) {
            const [thing, channelName] = channel

            await ChannelSubscriber.subscribe(thing, channelName, callback)

            return {
                stop() {
                    ChannelSubscriber.unsubscribe(thing, channelName)
                }
            }
        },
        async autoWatchChannel(channelProperty, callback) {
            let watcher = null

            this.$watch(
                channelProperty,
                async function (value) {
                    if (watcher !== null) {
                        watcher.stop()
                    }

                    watcher = await this.watchChannel(value, callback)
                },
                {
                    immediate: true
                }
            )
        },
        async applyChannel(channel, value) {
            const [thing, channelName] = channel

            const result = await axios.put(`/api/things/${thing}/channels/${channelName}`, value)

            if (!result.data) {
                return false
            }

            return true
        }
    }
}
