<template>
    <div class="dashboard">
        <!--        <nav class="navbar">-->
        <!--          <span class="brand">QOZY</span>-->
        <!--          <ul class="menu horizontal">-->
        <!--              <li v-if="editMode">-->
        <!--                  <a @click="showAddTileModal = true; addTileTile = null">-->
        <!--                      <icon icon="plus-square"></icon>-->
        <!--                  </a>-->
        <!--              </li>-->
        <!--              <li v-if="editMode">-->
        <!--                  <a @click="showSettingsModal = true">-->
        <!--                      <icon icon="cogs"></icon>-->
        <!--                  </a>-->
        <!--              </li>-->
        <!--              <li>-->
        <!--                  <input type="checkbox" :checked="editMode" @input="$store.dispatch('dashboard/setEditMode', $event.target.checked)">-->
        <!--              </li>-->
        <!--          </ul>-->
        <!--        </nav>-->

        <modal v-if="showSettingsModal" @close="showSettingsModal = false">
            <form>
                <div>
                    <label>Rows:</label>
                    <select v-model="rows">
                        <option v-for="value in 12" :key="value" :value="value">{{value}}</option>
                    </select>
                </div>
                <div>
                    <label>Columns:</label>
                    <select v-model="columns">
                        <option v-for="value in 12" :key="value" :value="value">{{value}}</option>
                    </select>
                </div>
            </form>
        </modal>

        <modal v-if="showAddTileModal" @close="showAddTileModal = false">
            <tile-settings v-model="addTileTile"></tile-settings>
            <button @click="addTile(addTileTile)">Save</button>
        </modal>

        <div class="grid" :class="'grid-' + size.width + 'x' + size.height">
            <tile v-for="(tile, index) in tiles" :tile="tile" @add-control="addControl(tile, $event)"></tile>
        </div>
    </div>
</template>

<script>
    import axios from "axios"

    import Tile from "./Tile.vue";
    import TileSettings from "@/components/forms/TileSettings/TileSettings.vue";
    import Modal from "@/components/Modal.vue";

    import {mapState, mapGetters} from 'vuex'

    export default {
        name: "dashboard",
        components: {Tile, TileSettings, Modal},
        props: {
            id: {
                required: true
            }
        },
        data() {
            return {
                // columns: 4,
                // rows: 4,
                showSettingsModal: false,
                showAddTileModal: false,
                addTileTile: {},
                showAddControlModal: false,
                // tiles: [
                //   {
                //     position: {
                //       row: null,
                //       column: null
                //     },
                //     size: {
                //       width: 2,
                //       height: 2
                //     },
                //     controls: [
                //       {
                //         type: "Graph",
                //         settings: {
                //           type: "area",
                //           yMax: 100,
                //           yMin: 0,
                //           items: [
                //             "item:thing:bridge:ssh:f76bccf7-1b34-47b4-ae32-73451d4840fc:1:cpuusage"
                //           ]
                //         }
                //       }
                //     ]
                //   },
                //   {
                //     position: {
                //       row: null,
                //       column: null
                //     },
                //     size: {
                //       width: 1,
                //       height: 1
                //     },
                //     controls: [
                //       {
                //         type: "String",
                //         settings: {
                //           item: "item:thing:bridge:ssh:f76bccf7-1b34-47b4-ae32-73451d4840fc:1:uptime"
                //         }
                //       }
                //     ]
                //   },
                //   {
                //     position: {
                //       row: 2,
                //       column: 3
                //     },
                //     size: {
                //       width: 1,
                //       height: 1
                //     },
                //     controls: [
                //       {
                //         type: "String",
                //         settings: {
                //           item: "item:thing:bridge:ssh:f76bccf7-1b34-47b4-ae32-73451d4840fc:1:uptime"
                //         }
                //       }
                //     ]
                //   },
                //   {
                //     position: {
                //       row: null,
                //       column: null
                //     },
                //     size: {
                //       width: 4,
                //       height: 1
                //     },
                //     controls: [
                //       {
                //         type: "Switch",
                //         settings: {
                //           item: "item:thing:bridge:wifiled:15058895-08c1-44a7-a8d1-9011c23db41b:6001948C9297:power"
                //         }
                //       },
                //       {
                //         type: "Color",
                //         settings: {
                //           item: "item:thing:bridge:wifiled:15058895-08c1-44a7-a8d1-9011c23db41b:6001948C9297:color"
                //         }
                //       },
                //       {
                //         type: "Dimmer",
                //         settings: {
                //           item: "item:thing:bridge:wifiled:15058895-08c1-44a7-a8d1-9011c23db41b:6001948C9297:coldwhite"
                //         }
                //       },
                //     ]
                // },
                // ]
            };
        },
        computed: {
            ...mapState('dashboard', [
                'dashboard',
                'editMode'
            ]),
            ...mapGetters('dashboard', [
                'size',
                'tiles'
            ])
        },
        methods: {
            addTile(tile) {
                this.tiles.push(tile)
                this.showAddTileModal = false
            },
            addControl(tile, control) {
                if (!tile.controls) {
                    tile.controls = []
                }

                tile.controls.push(control)
            }
        },
        watch: {
            dashboard: {
                handler: async function (value, oldValue) {
                    await axios.patch(`/plugins/dashboard/api/${this.id}`, value)
                },
                deep: true
            }
        },
        mounted() {
            this.$store.dispatch("dashboard/loadDashboard", this.id)
        }
    };
</script>

<style lang="scss">
    .dashboard {
        min-height: calc(100% - 100px);

        > .grid {
            padding: 10px;
        }
    }
</style>
