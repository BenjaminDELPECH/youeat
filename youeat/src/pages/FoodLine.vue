<template>
  <div class="" style="background-color:unset !important;">
    <div class="row q-mb-xs no-wrap">
      <div style="width:30px;">
        <q-checkbox
          v-if="canEdit"
          :val="elem.id"
          v-model="checkedFoodIdProxy"
        />
      </div>

      <div>
        <div class="flex no-wrap q-ml-xs">
          <div>
            <q-input
              standout
              v-if="canEdit"
                class="border1"
              type="number"
              dense

              borderless
              @input="updateLinkMealFood"
              v-model="quantity"
              style="width:30px;padding-left:10px;"
            />
            <span v-else>{{ quantity }} </span>
          </div>
          <div class="flex">
            <div style="margin:auto;">x</div>
          </div>
        </div>
      </div>

      <div>
        <q-select
          standout
          class="border1"
          v-if="canEdit"
          @input="updateLinkMealFood"
          borderless

          :options="optionsConversionFactors"
          dense
          v-model="conversionFactorSelected"
          style="padding-left:3px;width:100px;"
        />
        <span v-else>{{ measureName }}</span>


      </div>
      <div class="flex link1"
           @click="goToObjId('/food',elem.food_id)">
        <div class="q-pl-sm" style="margin:auto;">{{ elem.foodNameFr }}</div>
      </div>
    </div>

  </div>


</template>
<script>
export default {
  name: 'FoodLine',
  props: {
    checkedFoodId: {},
    elem: {},
    canEdit: {},
    conversionFactorsProp: []
  },
  data() {
    return {
      checkedFoodIdModel: -1,
      quantity: -1,
      conversionFactorSelected: -1
    }
  },
  methods: {
    goToObjId(path, id) {
      this.$router.push({
        path: path + "/" + id,

      })
    },
    toggleCheckFoodId() {
      this.$emit('toggleCheckFoodId', this.elem.id)
    },
    updateLinkMealFood() {
      if (this.quantity) {
        const variables = {
          "id": this.elem.id,
          "conversionFactorId": this.conversionFactorSelected.value,
          "quantity": this.quantity
        }
        this.$emit('updateLinkMealFood', variables)
      }
    }
  },
  computed: {
    conversionFactors() {
      console.log(this.conversionFactorsProp)
      const test =  this.conversionFactorsProp.filter(e => e.food_id === this.elem.food_id)
      return test
    },
    optionsConversionFactors() {
      const options =  this.conversionFactors.map(e => {
        return {
          "label": e.nameFr,
          "value": e.conversion_factor_id
        }
      })
      console.log(options)
       this.conversionFactorSelected = options.find(e => e.value === this.elem.conversion_factor_id)
      return options
    },
    checkedFoodIdProxy: {
      get() {
        return this.checkedFoodId.indexOf(this.elem.id) !== -1
      },
      set(newVal) {
        this.toggleCheckFoodId()
      }
    },
    options() {
      return this.elem.conversionFactors
    },

    measureName() {
      const test = this.elem.conversionFactors.find(e => e.conversion_factor_id === this.elem.conversion_factor_id)
      return test.nameFr
    }
  },
  watch: {
    elem() {
      console.log(this.elem.foodNameFr + " change")
    }
  },

  created() {

    this.conversionFactorSelected = this.optionsConversionFactors.find(e => e.value === this.elem.conversion_factor_id)
    this.quantity = this.elem.quantity
  }
}
</script>
