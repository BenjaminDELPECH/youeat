<template>
  <div>
    <div class="full-width flex header-custom" v-show="!searchMode" style="flex-flow: nowrap">

      <q-btn
        flat
        icon="arrow_back"

        @click="goBack"
      />

      <div class="flex" style="flex-flow: nowrap;margin:auto;">
        <div style="margin:auto;">
          {{ food.name_fr }}
        </div>
        <div class="q-ml-auto flex">
          <q-input
            type="number"
            dense
            v-model="quantity"
            @input="changeQuantity"
            style="width:40px;padding-left:10px;margin-right:8px;"
          />
          <q-select
            :options="optionsConversionFactors"
            dense
            v-model="conversionFactorSelected"/>
        </div>
      </div>
    </div>
    <NutrientStats
      :lmfs="lmfs"
      :lnf="lnf"
    />
  </div>
</template>

<script>
import NutrientStats from "components/NutrientStats";
import {fetchGoApi} from "src/utils/api";

export default {
  name: "FoodView",
  components: {NutrientStats},
  data() {
    return {
      lnf: [],
      food: {},
      conversionFactors: [],
      quantity: 1,
      lastQuantity : 1,
      conversionFactorSelected: undefined,
      optionsConversionFactors:[]
    }
  },
  methods: {
    changeQuantity(newVal){
      if(!!newVal) {
        this.lastQuantity = this.quantity
      }
    },
    goBack() {
      this.$router.go(-1)
    },
    fetchMealDatas() {
      const cpmt = this

      let callback = (response) => {
        cpmt.food = response[0]
      }
      let parameters = {"food_id": this.foodId}
      fetchGoApi(cpmt, 'getFood', 'food', parameters, callback)


      parameters = {"foodId": this.foodId}
      fetchGoApi(cpmt, 'getLNFByFoodId', 'lnf', parameters);

      let arr = []
      arr.push(this.foodId)
      parameters = {"food_id_list": arr}
      callback = (response) => {
        cpmt.conversionFactors = response

        cpmt.optionsConversionFactors = response.map(e => {
          return {
            "label": e.nameFr,
            "value": e.conversion_factor_id
          }
        })
        cpmt.conversionFactorSelected =  cpmt.optionsConversionFactors[0]
      }
      fetchGoApi(cpmt, 'getConversionFactors', 'conversionFactors', parameters, callback)

    },
    updateFoodLmf() {
      console.log("hello world")
    }
  },
  computed: {
    searchMode() {
      return this.$store.getters['layout/getSearchMode']
    },
    lmfs() {
      const lmfs = []
      const quantity = this.quantity ? this.quantity : this.lastQuantity
      if (this.conversionFactors.length && this.lnf.length && this.food && this.conversionFactorSelected &&  this.conversionFactorSelected.value) {
        console.log(this.food)
        const firstConversionFactor = this.conversionFactors.find(e => e.conversion_factor_id === this.conversionFactorSelected.value)
        const oneLMF = {}
        for (var convFactorObjKey in firstConversionFactor) {
          let propName = convFactorObjKey
          if (convFactorObjKey === "nameFr") {
            propName = "measureNameFr"
          }
          oneLMF[propName] = firstConversionFactor[convFactorObjKey]
        }
        oneLMF["foodNameFr"] = this.food["name_fr"]
        oneLMF["food_id"] = this.food.id
        oneLMF["quantity"] = quantity
        lmfs.push(oneLMF)
        return lmfs
      }
      return lmfs

    },
    foodId() {
      return this.$route.params.id
    }
  },
  created() {
    this.fetchMealDatas()

  }
}
</script>

<style scoped>

</style>
