<template>
    <div class="graph" ref="graph"></div>
</template>

<script>
import c3 from "c3";

export default {
  name: "graph",
  props: {
    options: {
      required: false,
      default: null
    },
    columns: {
      required: false
    },
    type: {
      required: false,
      default: "line"
    },
    xAxis: {
      required: false,
      default: false,
      type: Boolean
    },
    yAxis: {
      required: false,
      default: false,
      type: Boolean
    },
    axis: {
      required: false,
      default: null,
      type: Boolean
    },
    xGrid: {
      required: false,
      default: false,
      type: Boolean
    },
    yGrid: {
      required: false,
      default: false,
      type: Boolean
    },
    yMax: {
        required: false,
        default: null,
    },
    yMin: {
        required: false,
        default: null,
    },
    grid: {
      required: false,
      default: null,
      type: Boolean
    },
    tooltip: {
      required: false,
      default: false,
      type: Boolean
    },
    legend: {
      required: false,
      default: false,
      type: Boolean
    },
    point: {
      required: false,
      default: false,
      type: Boolean
    },
    height: {
      required: false,
      default: 150
    },
    width: {
      required: false,
      default: null
    },
    size: {
        required: false,
        default: null
    }
  },
  data() {
    return {
      chart: null
    };
  },
  watch: {
    columns() {
      this.chart.load(this.buildData())
    },
    type() {
      this.chart.transform(this.type);
    },
    size() {
        this.chart.resize({
            width: this.size ? this.size[0] : this.width,
            height: this.size ? this.size[1] : this.height,
        })
    },
    width() {
        this.chart.resize({
            width: this.size ? this.size[0] : this.width,
        })
    },
    height() {
        this.chart.resize({
            height: this.size ? this.size[1] : this.height,
        })
    }
  },
  methods: {
    buildData() {
      return {
        columns: this.columns,
        type: this.type,
        colors: {
            history: '#CDDC39'
        }
      };
    },
    buildOptions() {
      let options = {}

      if (this.options) {
        options = this.options
      } else {
        let showXAxis = this.axis ? this.axis : this.xAxis
        let showYAxis = this.axis ? this.axis : this.yAxis
        let showXGrid = this.grid ? this.grid : this.xGrid
        let showYGrid = this.grid ? this.grid : this.yGrid

        options = {
          data: this.buildData(),
          axis: {
            x: { show: showXAxis },
            y: { show: showYAxis, max: this.yMax, min: this.yMin, padding: {top: 0, bottom: 0} }
          },
          grid: {
              x: { show: showXGrid },
              y: { show: showYGrid },
          },
          tooltip: {
            show: this.tooltip
          },
          legend: {
            show: this.legend
          },
          point: {
            show: this.point
          },
          size: {
              width: this.size ? this.size[0] : this.width,
            height: this.size ? this.size[1] : this.height,
          }
        };
      }

      options["bindto"] = this.$refs.graph

      return options
    }
  },
  mounted() {
    this.chart = c3.generate(this.buildOptions())
  }
};
</script>

<style lang="scss">
</style>
