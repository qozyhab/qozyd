<template>
    <div class="control-color-settings">
        <channel-select v-model="settings.channel" :filter="channelFilter"></channel-select>
    </div>
</template>

<script>
import ControlSettings from "./ControlSettings.js"
import ChannelSelect from "@/components/ChannelSelect.vue"

export default {
  name: "ControlColorSettings",
  mixins: [ControlSettings],
  components: {ChannelSelect},
  methods: {
      channelFilter(channel) {
          return channel.type == 'ColorChannel'
      },
      validate() {
          return this.settings.channel != null
      }
  }
}
</script>

<style lang="scss">
</style>
