class Subscription {
    constructor(subscriber, thing, channel) {
        this.subscriber = subscriber
        this.thing = thing
        this.channel = channel
        this.callbacks = []
    }

    addListener(callback) {
        this.callbacks.push(callback)
    }

    removeListener(callback) {
        this.callbacks.splice(this.callbacks.indexOf(callback), 1)
    }

    notify(value, oldValue) {
        this.callbacks.forEach(callback => {
            callback({
                value: value,
                oldValue: oldValue
            })
        })
    }

    subscribe() {
        this.subscriber.webSocket.send(JSON.stringify({
            "type": "subscribe",
            "payload": {
                "thing_id": this.thing,
                "channel_name": this.channel
            }
        }))
    }

    unsubscribe() {
        this.subscriber.webSocket.send(JSON.stringify({
            "type": "unsubscribe",
            "payload": {
                "thing_id": this.thing,
                "channel_name": this.channel
            }
        }))
    }
}


class ChannelSubscriber {
    constructor() {
        this.subscriptions = {}
        this.connect()
    }

    static websocketUrl() {
        let protocol = "ws";
        let host = location.host;

        if (location.protocol === "https") {
            protocol = "wss"
        }

        return `${protocol}://${host}/api/channels/ws`
    }

    connect() {
        this.webSocket = new WebSocket(ChannelSubscriber.websocketUrl())
        this.webSocketPromise = new Promise((resolve) => {
            this.webSocket.onopen = () => {
                resolve()

                Object.values(this.subscriptions).forEach(subscription => {
                    subscription.subscribe()
                })
            }

            this.webSocket.onmessage = (e) => {
                const data = JSON.parse(e.data)

                const thingId = data.payload.thing_id
                const channelName = data.payload.channel_name

                const channelId = thingId + ":" + channelName

                this.subscriptions[channelId].notify(data.payload.value, data.payload.old_value)
            }

            this.webSocket.onclose = () => {
                setTimeout(() => {
                    this.connect()
                }, 2000)
            }
        })
    }

    async subscribe(thing, channel, callback) {
        await this.webSocketPromise

        const channelId = thing + ":" + channel

        let subscription = this.subscriptions[channelId]

        if (!subscription) {
            subscription = new Subscription(this, thing, channel)

            this.subscriptions[channelId] = subscription
        }

        subscription.addListener(callback)
        subscription.subscribe()

        return subscription
    }

    unsubscribe(thing, channel, callback) {
        const channelId = thing + ":" + channel
        const subscription = this.subscriptions[channelId]
        subscription.removeListener(callback)

        if (subscription.callbacks.length == 0) {
            subscription.unsubscribe()

            delete this.subscriptions[channelId]
        }
    }
}

export default new ChannelSubscriber()
