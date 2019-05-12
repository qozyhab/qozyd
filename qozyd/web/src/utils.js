import EventBus from "./event-bus.js"

export const Confirm = async (title, message) => {
    const promise = new Promise((resolve) => {
        EventBus.$emit("confirm", title, message, resolve)
    })

    return await promise
}

export const Toast = (text, interval = 5000) => {
    EventBus.$emit("toast", text, interval)
}
