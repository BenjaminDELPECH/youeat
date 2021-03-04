<template>
  <div class="" style="width:100%;" v-if="lmfs && lmfs.length && lnf.length && nutrients.length">

    <div class="">

      <div flat class=" q-ma-xs q-pa-xs " style="flex-flow:nowrap;"
           v-for="nutrientGrpWithNutrientVals in nutrientGrpsWithNutrientVals" :key="nutrientGrpWithNutrientVals.id">

        <div class=" text-subtitle2">
          {{ nutrientGrpWithNutrientVals.nameFr }}
        </div>

        <div  class="flex " style="width:100%;">
          <div  v-for="nutrient in nutrientGrpWithNutrientVals.nutrients"
               :name="nutrient.nameFr"
                class=" full-width"
          >


              <BarStat :nutrientName="nutrient.code" :nominator="nutrient.nutrientVal" :denominator="nutrient.besoin"
                       :showUnit="nutrient.nutrientGroupTitle==='1'" :unit="nutrient.unit"/>

          </div>
        </div>
      </div>


    </div>

  </div>
</template>

<script>
import {getCalory} from "src/utils/macroNutrients";

const calorieId = 208
const macroNutrientIds = ['1', '2', '3', '8']
const mapMacroProfileProp = [
  {propName: "carbohydrateProportion", nutrient_id: 205},
  {propName: "fatProportion", nutrient_id: 204},
  {propName: "proteinProportion", nutrient_id: 203},
]
import BarStat from "components/BarStat";

export default {
  name: "NutrientStats",
  components: {BarStat},
  props: {
    lmfs: {},
    lnf: {}
  },
  computed: {
    nutrients() {
      return this.$store.getters['nutrients/getNutrients']
    },
    nutrientGrps() {
      return this.$store.getters['nutrients/getNutrientGrps']
    },
    profile() {
      return this.$store.getters['user/getProfile']
    },
    nutrientGrpsWithNutrientVals() {
      const cpmt = this
      let nutrientGrpsWithNutrientVals = []
      let tmpNutrient = JSON.parse(JSON.stringify(this.nutrients))

      nutrientGrpsWithNutrientVals = this.nutrientGrps.map(e => {

        e.nutrients = []
        return e
      })


      tmpNutrient
        .forEach(nutrient => {
          nutrient.nutrientVal = 0
          nutrient.id = parseInt(nutrient.id.toString())
        })

      cpmt.lnf
        .forEach(lnf => {
          const {food_id, nutrient_id, value} = lnf
          const nutrientTarget = tmpNutrient.find(e => e.id === nutrient_id)
          if (nutrientTarget) {
            const lmfTarget = cpmt.lmfs.find(e => e.food_id === food_id)
            const {conversion_factor, quantity} = lmfTarget
            const nutrientVal = conversion_factor * quantity * value
            nutrientTarget.nutrientVal += nutrientVal
          }
        })
      tmpNutrient = tmpNutrient.filter(e => e.nutrientVal)

      function ifThisAMacroCheckIfThisIsAnUtrientGroupTitle(nutrient) {
        const {nutrientGroup_id, nutrientGroupTitle} = nutrient
        for (let i = 0; i < macroNutrientIds.length; i++) {
          const e = macroNutrientIds[i]
          if (nutrientGroup_id.toString() === e && nutrientGroupTitle !== "1") {
            return false
          }
        }
        return true
      }

      tmpNutrient.forEach(nutrient => {
        const {nutrientGroup_id} = nutrient
        if (nutrient.nutrientVal > 0) {
          if (ifThisAMacroCheckIfThisIsAnUtrientGroupTitle(nutrient)) {
            const targetGrpId = macroNutrientIds.indexOf(nutrientGroup_id.toString()) === -1 ? nutrientGroup_id : 10
            nutrientGrpsWithNutrientVals.find(e => e.id.toString() === targetGrpId.toString()).nutrients.push(nutrient)
          }
        }
      })

      const caloryNeed = getCalory(this.profile)


      mapMacroProfileProp.forEach(e2 => {
        const {propName, nutrient_id} = e2
        const macroProportion = cpmt.profile[propName]
        let coeff;
        if (nutrient_id === 205) {
          coeff = 4;
        }
        if (nutrient_id === 204) {
          coeff = 9;
        }
        if (nutrient_id === 203) {
          coeff = 4;
        }
        const macroNeed = (caloryNeed * macroProportion / 100) / coeff
        const targetNutrient = nutrientGrpsWithNutrientVals.find(e => e.id.toString() === "10").nutrients.find(e => e.id.toString() === nutrient_id.toString())
          if(targetNutrient){
            targetNutrient.besoin = macroNeed
          }

        nutrientGrpsWithNutrientVals.find(e => e.id.toString() === "10").nutrients.forEach(e => e.code = e.nameFr)
      })

      const allowedNutrientGroupId = [1, 2, 3, 4, 5, 10]
      nutrientGrpsWithNutrientVals = nutrientGrpsWithNutrientVals
        .filter(e => allowedNutrientGroupId.indexOf(parseInt(e.id)) !== -1 && e.nutrients.length)
        .sort((a, b) => {
          const diff = a.position - b.position
          if (diff === 0) return 0
          else if (diff > 0) return 1
          else return -1
        })

      console.log(nutrientGrpsWithNutrientVals)


      return nutrientGrpsWithNutrientVals
    }
  },
  methods: {
    searchFoods() {
      this.$store.commit('layout/updateSearchPageTabSelected', "food")
      this.$store.commit('layout/updateSearchMode', true)
      this.$store.commit('layout/updateMealIdSelected', this.meal.id)
    },
  }
}
</script>
<style>

</style>

