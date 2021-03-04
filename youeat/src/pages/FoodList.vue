<template>
  <div class=" q-pb-xl" style="">
    <div class="flex" style="width:100%;height:50px;" v-if="canEdit">
      <div class="" style="margin-top:auto; margin-bottom:auto;">
        <q-checkbox

          v-model="checkedAll" @input="toggleCheckAll"/>
      </div>
      <div
        v-show="!checkedFoodId.length"
        class="q-pa-sm"
        style="white-space: nowrap">
        <q-btn label="Ajouter aliment" size="md"
               dense

               flat
               @click="searchFoods"
        />
      </div>
      <q-btn v-show="checkedFoodId.length" name="delete" icon="delete" flat @click="confirmDelete"/>
    </div>
    <FoodLine
          v-if="conversionFactors.length"
          v-for="elem in foods"
          :canEdit="canEdit"
          :class="backgroundClass(elem.i)"
          :conversion-factors-prop="conversionFactors"
          :checked-food-id="checkedFoodId" :elem="elem"
          @updateLinkMealFood="updateLinkMealFood"
          @toggleCheckFoodId="toggleCheckFoodId"
        />
    <div v-if="wantDeleteFoodId">
      <ConfirmDialog
        label="Voulez-vous vraiment supprimmer ces aliments de votre repas?"
        icon-name="delete"
        :confirm-action="confirmDelete"
        :cancel-action="cancelDelete"
      />
    </div>

  </div>
</template>
<script>
import ConfirmDialog from "components/ConfirmDialog";
import {callGoApi} from "src/utils/api";
import FoodLine from "pages/FoodLine";

export default {
  name: 'FoodList',
  components: {FoodLine, ConfirmDialog},
  props: {
    lmfs: {},
    canEdit: {}
  },
  data() {
    return {
      checkedAll: false,
      checkedFoodId: [],
      wantDeleteFoodId: false,
      conversionFactors: []
    }
  },
  methods: {
    searchFoods() {
      // this.$store.commit('layout/updateSearchPageTabSelected', "food")
      // this.$store.commit('layout/updateSearchMode', true)
      // this.$store.commit('layout/updateMealIdSelected', this.mealId)
      this.$emit("wantSearchFood")
    },
    toggleCheckFoodId(lmfId) {
      const index = this.checkedFoodId.findIndex(e => e === lmfId)
      if (index !== -1) {
        this.checkedFoodId.splice(index, 1)
        if (!this.checkedFoodId.length) this.checkedAll = false
      } else {
        this.checkedFoodId.push(lmfId)
      }
    },

    updateLinkMealFood(variables) {
      this.$emit('updateLinkMealFood', variables)
    },
    confirmDelete() {
      this.$store.dispatch('meals/deleteLinkMealFoodFunc', {
        linkMealFoodIdList: this.checkedFoodId
      })
      this.wantDeleteFoodId = false

      this.$emit('deleteLinkMealFoodList', this.checkedFoodId)
      this.checkedFoodId = []
      this.checkedAll = false
    },
    cancelDelete() {
      this.wantDeleteFoodId = false
    },
    toggleCheckAll(value) {
      if (value === true && this.checkedFoodId.length) {
        this.checkedFoodId = []
        this.checkedAll = false
      } else {
        this.checkedFoodId = this.lmfs.map(e => e.id)
      }
    },
    backgroundClass(index) {
      const evenNumber = index % 2 === 0
      const color = evenNumber ? "green-1" : "white"
      return "bg-" + color
    },
    fetchConversionFactors: function () {
      const callback = (data) => {
        this.conversionFactors = data
      }
      const parameters = {"food_id_list": this.lmfs.map(e => e.food_id)}
      callGoApi(this, "/getConversionFactors", callback, parameters)
    },
  },
  computed: {

    mealId() {
      return this.lmfs[0].meal_id
    },
    foods() {

      if (this.conversionFactors) {
        this.lmfs.forEach(lmf => {
          lmf.conversionFactors = this.conversionFactors.filter(e => e.food_id === lmf.food_id)
        })
      }
      return this.lmfs
    }
  },
  watch: {
    checkedFoodId() {
      if (this.checkedFoodId.length) this.checkedAll = null
    },
    searchMode() {
      this.fetchConversionFactors()
    },
    foods(){
      const isFoodWithoutConversioNFactor = this.foods.find(e=>e.conversionFactors.length === 0)
      if(isFoodWithoutConversioNFactor){
        this.fetchConversionFactors()
      }
    }
  },
  mounted() {
    console.log(this.lmfs)
  },

  created() {
    this.fetchConversionFactors();
  }
}
</script>
