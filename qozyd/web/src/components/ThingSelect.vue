<template>
    <div class="thing-select">
        <ul class="list-group" v-if="things">
            <li class="list-item" v-for="(thing, thingId) in doFilter(things)" :key="thingId"
                @click="$emit('input', thing.id)" :class="{ active: value == thing.id }">
                <div v-if="thing.name">
                    <div>{{ thing.name }}</div>
                    <small>({{ thing.id }})</small>
                </div>
                <div v-else>{{ thing.id }}</div>
            </li>
        </ul>
    </div>
</template>

<script>
    import axios from "axios"

    export default {
        name: "ThingSelect",
        props: ["value", "filter"],
        data() {
            return {
                things: null
            }
        },
        methods: {
            async loadThings() {
                if (this.things != null) {
                    return this.things
                }

                let result = await axios.get("/api/things")
                const thingIds = result.data

                this.things = {}
                await thingIds.forEach(async thingId => {
                    let result = await axios.get(`/api/things/${thingId}`)
                    const thing = result.data
                    this.things[thingId] = thing

                    this.$forceUpdate()
                });
            },
            doFilter(things) {
                if (this.filter) {
                    return Object.values(this.things).filter(this.filter).reduce((result, thing) => {
                        result[thing.id] = thing
                        return result
                    }, {})
                }

                return things
            }
        },
        async mounted() {
            await this.loadThings()
        }
    }
</script>

<style lang="scss">
</style>
