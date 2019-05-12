<template>
    <span class="editable-text">
        <span v-if="!editMode">{{value || placeholder}}</span>
        <input ref="editInput" type="text" v-show="editMode" :value="value" @keydown.enter="save($event)" @keydown.esc="abort()">
        <icon @click="enableEditMode()" class="edit-icon cursor-pointer ml-2" fixed-width icon="edit"></icon>
    </span>
</template>

<script>
    export default {
        name: "EditableText",
        props: {
            value: {
                type: String
            },
            placeholder: {
                type: String
            }
        },
        methods: {
            enableEditMode() {
                this.editMode = true
                setTimeout(() => {this.$refs.editInput.focus()}, 0)
            },
            abort() {
                this.editMode = false
            },
            save($event) {
                this.$emit('input', $event.target.value)
                this.editMode = false
            }
        },
        data() {
            return {
                editMode: false
            }
        }

    }
</script>

<style lang="scss">
    .editable-text {
        > .edit-icon {
            display: none;
        }

        &:hover {
            > .edit-icon {
                display: initial;
            }
        }

        > input {
            display: inline;
            width: auto;
        }
    }
</style>
