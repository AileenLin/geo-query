<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '300px'
    },
    height: {
      type: String,
      default: '300px'
    },
    aiData: {
      type: Number,
      default: 0.0
    },
    nlpData: {
      type: Number,
      default: 0.0
    },
    mlData: {
      type: Number,
      default: 0.0
    },
    itData: {
      type: Number,
      default: 0.0
    },
    visionData: {
      type: Number,
      default: 0.0
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    aiData: function(newVal, oldVal) { // watch it
      this.initChart()
    },
    nlpData: function(newVal, oldVal) { // watch it
      // console.log('Prop changed: ', newVal, ' | was: ', oldVal)
    },
    visionData: function(newVal, oldVal) { // watch it
      // console.log('Prop changed: ', newVal, ' | was: ', oldVal)
    },
    mlData: function(newVal, oldVal) { // watch it
      // console.log('Prop changed: ', newVal, ' | was: ', oldVal)
    },
    itData: function(newVal, oldVal) { // watch it
      // console.log('Prop changed: ', newVal, ' | was: ', oldVal)
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')

      this.chart.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          left: 'center',
          bottom: '10',
          data: ['AI', 'Vision', 'MLMining', 'NLP', 'InfoRet']
        },
        series: [
          {
            name: 'Publications(ADJ)',
            type: 'pie',
            roseType: 'radius',
            radius: [15, 95],
            center: ['50%', '38%'],
            data: [
              { value: this.aiData, name: 'AI' },
              { value: this.visionData, name: 'Vision' },
              { value: this.mlData, name: 'MLMining' },
              { value: this.nlpData, name: 'NLP' },
              { value: this.itData, name: 'InfoRet' }
            ],
            animationEasing: 'cubicInOut',
            animationDuration: 2600
          }
        ]
      })
    }
  }
}
</script>
