<template>
    <div class="bridge-settings">
        <section class="tabs">
            <ol class="items">
                <router-link :to="{name: 'bridge_settings', props: {bridgeId: bridgeId}}" tag="li" exact-active-class="active"><icon icon="cogs" fixed-width></icon> Settings</router-link>
                <router-link :to="{name: 'bridge_settings.form', props: {bridgeId: bridgeId}}" tag="li" exact-active-class="active"><icon icon="flask" fixed-width></icon> Experimental</router-link>
            </ol>

            <div class="content card">
                <router-view></router-view>
            </div>
        </section>
    </div>
</template>

<script>
    export default {
        name: 'BridgeSettings',
        props: {
            bridgeId: {
                type: String,
                required: true
            }
        }
    }
</script>

<style lang="scss">

</style>
