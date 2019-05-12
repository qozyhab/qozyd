<template>
    <div v-if="active">
        <slot></slot>
    </div>
</template>

<script>
export default {
  name: "step",
  inject: ["wizard"],
  props: {
      validate: {
          required: false
      },
      title: {
          required: false
      },
      data: {
          required: false
      }
  },
  data() {
      return {
          active: false,
          index: null
      }
  },
  methods: {
      async doValidate() {
          if (this.validate) {
              return await this.validate()
          }

          return true
      }
  },
  mounted() {
      this.wizard.addStep(this)
  },
  destroyed() {
      this.wizard.removeStep(this)
  }
}
</script>

<style lang="scss">
</style>
