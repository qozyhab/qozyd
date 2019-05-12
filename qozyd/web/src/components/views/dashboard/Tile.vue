<template>
    <div class="tile" ref="tile" :class="['grid-row-' + tile.position.row, 'grid-col-' + tile.position.column, 'colspan-' + tile.size.width, 'rowspan-' + tile.size.height, {'vertical': tile.orientation == 'vertical'}]">
        <ul class="menu horizontal text-right">
            <li v-if="editMode">
                <a @click="showAddControlModal = true">
                    <icon icon="plus-square"></icon>
                </a>
            </li>
            <li v-if="editMode">
                <a @click="showEditTileModal = true">
                    <icon icon="cogs"></icon>
                </a>
            </li>
        </ul>

        <h1 class="title">{{tile.headline}}</h1>

        <div class="controls">
            <div class="control" v-for="control in tile.controls">
                <div class="value">
                    <control :control="control"></control>
                </div>
            </div>
        </div>

        <modal v-if="showAddControlModal" @close="showAddControlModal = false, addControlSettings = {}">
          <control-settings v-model="addControlSettings"></control-settings>
          <button @click="addControl(addControlSettings)">Save</button>
        </modal>

        <modal v-if="showEditTileModal" @close="showEditTileModal = false">
          <tile-settings v-model="tile"></tile-settings>
        </modal>
    </div>
</template>

<script>
import Control from "./controls/Control.vue"
import Modal from "@/components/Modal.vue";
import ControlSettings from "@/components/forms/ControlSettings/ControlSettings.vue";
import TileSettings from "@/components/forms/TileSettings/TileSettings.vue";

import { mapState } from 'vuex'


export default {
  name: "tile",
  components: { Control, Modal, ControlSettings, TileSettings },
  props: {
    tile: {
    },
  },
  data() {
    return {
      showAddControlModal: false,
      addControlSettings: {},
      showEditTileModal: false,
      widthUpdateInterval: null,
    }
  },
  methods: {
    addControl(control) {
      this.$emit("add-control", control)
      this.showAddControlModal = false
      this.addControlSettings = {}
    }
  },
  computed: {
    ...mapState('dashboard', [
      'editMode'
    ])
  },
  mounted() {
    const self = this;

    this.widthUpdateInterval = setInterval(() => {
      const width = this.$refs.tile.offsetWidth;

      if (width != self.width) {
        self.width = width
      }
    }, 100);
  },
  destroyed() {
    clearInterval(this.widthUpdateInterval)
  }
};
</script>

<style lang="scss">
.tile {
  background-color: #F5F5F5;
  padding: 20px 40px;

  > .title {
    text-transform: uppercase;
    font-size: 1.1rem;
    margin-bottom: 20px;
  }

  > .controls {
    display: flex;
    flex-direction: row;

    > .control {
      flex: 1;

      > .value {
        font-size: 1rem;
      }

      > .graph {
        max-width: 100%;
      }
    }
  }

  &.horizontal > .controls {
    flex-direction: row;
  }

  &.vertical {
    height: 100%;

    > .title {
      flex: 0;
    }

    > .controls {
      flex: 1;
      flex-direction: column;
    }
  }

  min-width: 0; /* NEW; needed for Firefox */
}
</style>
