<template>
    <div>
      <ol class="steps">
        <slot name="steps" v-for="step in steps" :step="step"></slot>
      </ol>

      <slot></slot>

      <slot name="buttons" v-if="showButtons" v-bind:wizard="wizard()">
          <button :disabled="!hasPreviousStep()" @click="toPreviousStep()">Prev</button>
          <button :disabled="!hasNextStep()" @click="toNextStep()">Next</button>
          <button :disabled="hasNextStep()" @click="finish()">Finish</button>
      </slot>
    </div>
</template>

<script>
export default {
  name: "wizard",
  props: {
    showButtons: {
        default: true
    }
  },
  data() {
    return {
      steps: [],
      currentStepIndex: null
    }
  },
  provide() {
    return {
      wizard: {
        addStep: step => {
          step.index = this.steps.length
          this.steps.push(step)
        },
        removeStep: step => {
          this.steps.splice(this.steps.indexOf(step))
        }
      }
    }
  },
  methods: {
    wizard() {
        return this;
    },
    initialize() {
      if (this.currentStepIndex == null && this.steps.length > 0) {
        this.setStep(0)
      }
    },
    getCurrentStep() {
      if (this.currentStepIndex == null) {
        return null
      }

      return this.steps[this.currentStepIndex]
    },
    getStep(index) {
      return this.steps[index]
    },
    setStep(index) {
      if (index >= 0 && index < this.steps.length && this.currentStepIndex != index) {
        if (this.getCurrentStep()) {
          this.getCurrentStep().active = false
        }

        this.currentStepIndex = index
        this.getStep(index).active = true
      }
    },
    hasNextStep() {
      return this.steps.length - 1 > this.currentStepIndex
    },
    hasPreviousStep() {
      return this.currentStepIndex > 0
    },
    async validate() {
      return await this.getCurrentStep().doValidate()
    },
    async toNextStep() {
      if (await this.validate() && this.hasNextStep()) {
        this.setStep(this.currentStepIndex + 1)
      }
    },
    toPreviousStep() {
      if (this.hasPreviousStep()) {
        this.setStep(this.currentStepIndex - 1)
      }
    },
    async finish() {
      if (!this.hasNextStep() && await this.validate()) {
        this.$emit('finish')
      }
    }
  },
  mounted() {
    this.initialize()
  }
}
</script>

<style lang="scss">
</style>
