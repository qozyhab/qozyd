<template>
    <div class="control-select row">
        <div class="col s3">
            <div class="control-type card hover" @click="$emit('input', 'Color')" :class="{active: value == 'Color'}">
                <icon icon="palette" size="3x"></icon>
                <div class="title">
                    Color
                </div>
            </div>
        </div>
        <div class="col s3">
            <div class="control-type card hover" @click="$emit('input', 'String')" :class="{active: value == 'String'}">
                <icon icon="font" size="3x"></icon>
                <div class="title">
                    Text
                </div>
            </div>
        </div>
        <div class="col s3">
            <div class="control-type card hover" @click="$emit('input', 'Dimmer')" :class="{active: value == 'Dimmer'}">
                <icon icon="sliders-h" size="3x"></icon>
                <div class="title">
                    Dimmer
                </div>
            </div>
        </div>
        <div class="col s3">
            <div class="control-type card hover" @click="$emit('input', 'Graph')" :class="{active: value == 'Graph'}">
                <icon icon="chart-bar" size="3x"></icon>
                <div class="title">
                    Graph
                </div>
            </div>
        </div>
        <div class="col s3">
            <div class="control-type card hover" @click="$emit('input', 'Switch')" :class="{active: value == 'Switch'}">
                <icon icon="toggle-on" size="3x"></icon>
                <div class="title">
                    Switch
                </div>
            </div>
        </div>
        <div class="col s3">
            <div class="control-type card hover" @click="$emit('input', 'Number')" :class="{active: value == 'Number'}">
                <icon icon="sort-numeric-up" size="3x"></icon>
                <div class="title">
                    Number
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "ControlSelect",
  props: ["value"]
}
</script>

<style lang="scss">
.control-select {
    .control-type {
        cursor: pointer;
        text-align: center;

        &.active {
            background-color: #e4e4e4;
        }

        > .title {
            font-weight: bold;
            margin-top: 10px;
        }
    }
}
</style>
