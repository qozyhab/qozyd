<template>
    <div class="control-settings">
        <wizard class="wizard">
            <template slot="steps" slot-scope="{ step }">
                <li :class="{ active: step.active }">
                    <div class="circle">{{ step.index + 1 }}</div>
                    {{ step.title }}
                </li>
            </template>

            <step :validate="validateControl" title="Control" class="control-type-step">
                <div class="row">
                    <label class="col s3">
                        Headline
                    </label>

                    <div class="col s9">
                        <input type="text" v-model="control.headline"/>
                    </div>
                </div>
                
                <control-select v-model="control.type"></control-select>
            </step>

            <step title="Settings" :validate="validateSettings">
                <component :is="settingsComponent" ref="settingsComponentInstance" v-model="control.settings"></component>
            </step>
        </wizard>
    </div>
</template>

<script>
import Wizard from "@/components/wizard/Wizard.vue"
import Step from "@/components/wizard/Step.vue"

import ControlSelect from "./ControlSelect.vue"
import ControlColorSettings from "./Settings/ControlColorSettings.vue"
import ControlSwitchSettingsVue from './Settings/ControlSwitchSettings.vue';
import ControlStringSettingsVue from './Settings/ControlStringSettings.vue';
import ControlDimmerSettingsVue from './Settings/ControlDimmerSettings.vue';
import ControlNumberSettingsVue from './Settings/ControlNumberSettings.vue';

const settingsComponents = {
    Color: ControlColorSettings,
    Switch: ControlSwitchSettingsVue,
    String: ControlStringSettingsVue,
    Dimmer: ControlDimmerSettingsVue,
    Number: ControlNumberSettingsVue
}

export default {
  name: "ControlSettings",
  components: {Wizard, Step, ControlSelect},
  props: {
      value: {
          required: false
      }
  },
  data() {
      return {
          control: this.value || {}
      }
  },
  watch: {
      control: {
          deep: true,
          handler: function (value) {
              this.$emit("input", value)
          }
      }
  },
  computed: {
      settingsComponent: function () {
          return settingsComponents[this.control.type]
      }
  },
  methods: {
      validateControl() {
          return this.control.type != null
      },
      validateSettings() {
          return this.$refs.settingsComponentInstance.validate()
      },
      save() {
          this.$emit("input", {
              type: this.controlType,
              settings: this.settings
          })
      }
  }
};
</script>

<style lang="scss">
$step-spacing: 50px;

.control-settings {
    > .wizard {
        > .steps {
            list-style: none;
            margin: 0;
            padding: 0;

            display: flex;
            flex-direction: row;

            > li {
                position: relative;
                text-align: center;
                margin: 0 $step-spacing;
                width: 80px;

                &::before {
                    position: absolute;

                    content: "";
                    top: 37.5px;
                    height: 5px;
                    left: -$step-spacing;
                    width: $step-spacing;

                    background-color: #e4e4e4;
                }

                &::after {
                    position: absolute;

                    content: "";
                    top: 37.5px;
                    height: 5px;
                    right: -$step-spacing;
                    width: $step-spacing;

                    background-color: #e4e4e4;
                }

                &.active {
                    &::after {
                        background-color: #fff;
                        border-top: 1px solid #e4e4e4;
                        border-bottom: 1px solid #e4e4e4;
                    }
                }

                &.active ~ li {
                    &::before {
                        background-color: #fff;
                        border-top: 1px solid #e4e4e4;
                        border-bottom: 1px solid #e4e4e4;
                    }

                    &::after {
                        background-color: #fff;
                        border-top: 1px solid #e4e4e4;
                        border-bottom: 1px solid #e4e4e4;
                    }
                }

                &:first-child {
                    margin-left: 0;

                    &::before {
                        display: none;
                    }
                }

                &:last-child {
                    margin-right: 0;

                    &::after {
                        display: none;
                    }
                }

                > .circle {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0 auto;

                    font-size: 1.4em;
                    font-weight: bold;
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;

                    border: 1px solid #e4e4e4;
                }

                &.active {
                    > .circle {
                        background-color: #e4e4e4;
                    }
                }
            }
        }

        // Steps
        > .control-type-step {
            .control-type {
                padding: 10px;

                &.active {
                    background-color: #e4e4e4;
                }
            }
        }
    }
}
</style>
