<template>

  <div class="q-mb-xs " style="width:100%;font-size:11px;">
    <div class="flex" style="width:100%;">
      <div style="">{{nutrientName}}</div>
      <div  :class="textColorClass" style="margin-left:auto;margin-right:10px;">{{ percentageText }}</div>
    </div>
    <div class="" style="">
      <div class="bg-grey-10"
           style="display:flex;flex-direction: column-reverse;height: 3px;margin:auto;border-radius: 2px;">
        <div :class="bgColorClass" :style="style">
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'BarStat',
  props: [
    'nominator', 'denominator', 'showUnit', 'unit','nutrientName'
  ],
  computed: {
    percentage() {
      let percentage = (this.nominator / this.denominator) * 100
      if (percentage > 100) percentage = 100
      return Math.round(percentage)
    },
    percentageText() {
      const nominator = Math.round(this.nominator)
      const denominator = Math.round(this.denominator)
      return (true ? " " + nominator + " / " + denominator + this.unit : this.percentage.toString())
    },
    getColorClass: function () {
      let colorClass = "";
      if (this.percentage > 90) {
        colorClass = "light-green-8"
      } else if (this.percentage > 50) {
        colorClass = "orange-9"
      } else if (this.percentage > 25) {
        colorClass = "deep-orange-9"
      } else {
        colorClass = "red-8"
      }
      return colorClass;
    },
    bgColorClass() {
      let colorClass = this.getColorClass;
      return "bg" + "-" + colorClass + ""
    },
    textColorClass() {
      return " text-caption"
    }
    ,
    style() {

      return "width:" + this.percentage + "%; height:100%;"
    }
  },
  methods: {}
}
</script>
