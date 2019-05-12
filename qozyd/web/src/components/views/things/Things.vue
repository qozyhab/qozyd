<template>
    <div class="things row">
        <div class="col-lg-2">
            <div class="card">
                <nav>
                    <ul class="menu vertical">
                        <li @click="scan()">
                            <icon icon="search" fixed-width></icon>
                            Discover new Things

                            <icon v-if="scanning" icon="spinner" spin fixed-width class="pull-right"></icon>
                        </li>
                        <li @click="find()">
                            <icon icon="compass" fixed-width></icon>
                            Find Things

                            <icon v-if="finding" icon="spinner" spin fixed-width class="pull-right"></icon>
                        </li>
                    </ul>
                </nav>
            </div>
        </div>
        <div class="col-lg-10">
            <div class="row">
                <div class="col-12">
                    <transition-group name="fade" tag="div">
                        <thing v-for="thing in things" :key="thing" :thing-id="thing" class="mb-2" @remove="removeThing(thing)"></thing>
                    </transition-group>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios"

    import Thing from "./Thing.vue"
    import {Toast} from "@/utils.js"

    export default {
        name: 'things',
        components: {Thing},
        data() {
            return {
                things: [],
                scanning: false,
                finding: false,
            }
        },
        methods: {
            async getThings() {
                const result = await axios.get("/api/things")

                return result.data
            },
            async scan() {
                this.scanning = true
                const result = await axios.get("/api/things/scan")
                const newThings = result.data

                this.things = await this.getThings()

                this.scanning = false

                if (newThings > 0) {
                    Toast("Found " + newThings + " new things")
                } else {
                    Toast("No new things found")
                }
            },
            async find() {
                this.finding = true

                await axios.get("/api/things/find")
                this.things = await this.getThings()

                this.finding = false
            },
            async removeThing(thingId) {
                await axios.delete(`/api/things/${thingId}`)

                this.things = await this.getThings()
            }
        },
        async mounted() {
            this.things = await this.getThings()
        }
    }
</script>

<style lang="scss">

</style>
