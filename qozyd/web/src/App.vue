<template>
    <div id="app">
        <transition-group name="fade" tag="section" class="toasts">
            <div class="toast" :key="toast.id" v-for="toast in toasts">
                {{toast.text}}
            </div>
        </transition-group>

        <nav class="navbar">
            <img src="@/assets/logo.svg" alt="qozy.io" class="brand">

            <ul class="menu horizontal">
                <li>
                    <router-link :to="{name: 'overview'}" exact>Overview</router-link>
                </li>
                <li>
                    <router-link :to="{name: 'bridges'}">Bridges</router-link>
                </li>
                <li>
                    <router-link :to="{name: 'things'}">Things</router-link>
                </li>
                <li>
                    <router-link :to="{name: 'rules'}">Rules</router-link>
                </li>
                <li>
                    <router-link :to="{name: 'plugins'}">Plugins</router-link>
                </li>
            </ul>
        </nav>

        <confirm ref="confirm"></confirm>

        <div class="container">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    class Toast {
        constructor(text) {
            this.id = Toast.id++
            this.text = text
        }
    }
    Toast.id = 0

    import EventBus from "./event-bus.js"
    import Confirm from "@/components/Confirm.vue"

    export default {
        name: 'app',
        components: {Confirm},
        data() {
            return {
                toasts: []
            }
        },
        mounted() {
            EventBus.$on("confirm", async (title, message, resolve) => {
                resolve(await this.$refs.confirm.open(title, message))
            })

            EventBus.$on("toast", (text, interval) => {
                const toast = new Toast(text)

                this.toasts.push(toast)

                if (interval > 0) {
                    setTimeout(() => {
                        this.toasts.splice(this.toasts.indexOf(toast), 1)
                    }, interval)
                }
            })
        }
    }
</script>

<style>
    html, body {
        height: 100%;
        margin: 0;
        padding: 0;

        font-family: sans-serif;
        color: #263238;
    }

    body {
        height: 100%;
        background-color: #ECEFF1;
    }

    #app {
        min-height: 100%;
    }

    #app:before, #app:after {
        content: ' ';
        display: table;
    }
</style>
