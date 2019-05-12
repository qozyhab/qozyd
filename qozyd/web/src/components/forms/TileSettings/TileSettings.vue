<template>
    <div class="tile-settings">
        <div class="row">
            <label class="col s3">
                Headline
            </label>

            <div class="col s9">
                <input type="text" v-model="tile.headline">
            </div>
        </div>

        <div class="row">
            <label class="col s3">
                Orientation
            </label>

            <div class="col s9">
                <select v-model="tile.orientation">
                    <option value="horizontal">Horizontal</option>
                    <option value="vertical">Vertical</option>
                </select>
            </div>
        </div>

        <div class="row">
            <label class="col s3">
                Column
            </label>

            <div class="col s9">
                <input type="number" v-model.number="tile.position.column">
            </div>
        </div>

        <div class="row">
            <label class="col s3">
                Row
            </label>

            <div class="col s9">
                <input type="number" v-model.number="tile.position.row">
            </div>
        </div>

        <div class="row">
            <label class="col s3">
                Width
            </label>

            <div class="col s9">
                <input type="number" v-model.number="tile.size.width">
            </div>
        </div>

        <div class="row">
            <label class="col s3">
                Height
            </label>

            <div class="col s9">
                <input type="number" v-model.number="tile.size.height">
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "TileSettings",
  props: {
      value: {
          required: false
      }
  },
  data() {
      return {
          tile: this.value || {position: {}, size: {}, controls: []}
      }
  },
  watch: {
      value: function (value) {
          this.tile = value
      },
      tile: {
          deep: true,
          handler: function (value) {
              this.$emit("input", value)
          }
      }
  }
};
</script>

<style lang="scss">
</style>
