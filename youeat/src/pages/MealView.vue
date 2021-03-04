<template>
  <div class="flex" v-if="!searchMode">

    <div v-show="!searchMode && !editMealNameMode && searchingFood"
    class=" full-width  no-wrap flex"
    >
      <q-btn
      flat
      icon="arrow_back"
      @click="cancelSearch"
    />
      <q-input
        class="q-pl-md"
        label="search" dense v-model="searchText"
        style="width:100%;"
        type="search" placeholder="Rechercher..."
        ref="searchInput"
        color="green"
      />
    </div>

    <div v-show="!searchMode && editMealNameMode && !searchingFood" class="flex no-wrap q-pl-xs" style="width:100%;">
      <q-input ref="editMealNameInput" type="text" label="Nom du repas" v-model="mealName"/>
      <div class="flex" style="margin:auto;">
        <q-icon name="save" size="sm" @click="saveMealName"/>
        <q-icon name="cancel" class="q-pl-lg" size="sm" @click="editMealNameMode=false"/>
      </div>
    </div>

    <div
      v-show="!searchMode && !editMealNameMode && !searchingFood"
      class="flex row borderBottom1 full-width no-wrap" bordered
      style="">

      <q-btn
        flat
        class="col-2"
        icon="arrow_back"
        @click="goBack()"
      />

      <div
        class="col-6 text-subtitle2"
        style="margin:auto 0;word-wrap: break-word;"
        v-if="meal && meal.name">
        <div>{{ mealName }}</div>


        <div class="text-caption">{{ author }}</div>
      </div>
      <div class="col-4 row">
        <div class="col-6">
          <q-btn
            @click="toggleSearchMode"
            flat
            icon="search"
          />
        </div>
        <div class="col-6">
          <q-btn-dropdown
            style=""
            dropdown-icon="more_vert"
            flat
            dense
          >
            <q-list>
              <q-item clickable v-close-popup @click="editMealNameMode=true">
                <q-item-section avatar>
                  <q-avatar icon="edit"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Renommer</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="deleteMeal">
                <q-item-section avatar>
                  <q-avatar icon="delete" text-color="red"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Suprimmer</q-item-label>
                </q-item-section>
              </q-item>

            </q-list>
          </q-btn-dropdown>
        </div>
      </div>
    </div>


    <div class="full-width" v-show="lmfs.length && !searchMode">
      <q-tabs class="sm-larger-hide " v-model="mealViewTabSelected" dense>
        <div class="flex q-mr-auto">
          <q-tab name="Stats" label="Stats"/>
          <q-tab name="Ingredients" label="Ingredients"/>
          <q-tab name="Resultats"
                 label="Résultats"/>
        </div>
      </q-tabs>

      <div class="flex q-pb-xl" v-show="mealViewTabSelected!=='Resultats'">
        <NutrientStats
          v-if="!largerThanSM"
          v-show="mealViewTabSelected==='Stats'"
          :lmfs="lmfs"
          :lnf="lnf"

        />
        <FoodList
          :can-edit="canEdit"
          v-if="!largerThanSM &&  lmfs.length"
          v-show="mealViewTabSelected==='Ingredients'"
          :lmfs="lmfs"
          :tab-model="mealViewTabSelected"
          @updateLinkMealFood="updateLinkMealFood"
          @deleteLinkMealFoodList="deleteLinkMealFoodList"
          @wantSearchFood="wantSearchFood"
        />
        <!--        <FoodList-->
        <!--          :can-edit="canEdit"-->
        <!--          class="col-6"-->
        <!--          v-if="largerThanSM && lmfs.length"-->
        <!--          :lmfs="lmfs"-->
        <!--          :tab-model="mealViewTabSelected"-->
        <!--          @updateLinkMealFood="updateLinkMealFood"-->
        <!--          @deleteLinkMealFoodList="deleteLinkMealFoodList"-->
        <!--        />-->
        <!--        <NutrientStats-->
        <!--          v-if="largerThanSM"-->
        <!--          class="col-6 q-pr-sml"-->
        <!--          :lmfs="lmfs"-->
        <!--          :lnf="lnf"-->

        <!--        />-->
      </div>
      <div v-show="mealViewTabSelected==='Resultats'" >
        <FoodListResult
          :foods="foods"
          :meal-id-selected="mealId"

        />
      </div>
    </div>


  </div>

</template>

<script>


import NutrientStats from "components/NutrientStats";
import {sendForm} from "src/utils/sendForm";
import FoodList from "pages/FoodList";
import {callGoApi, propsToLowerCase} from "src/utils/api";
import FoodListResult from "pages/FoodListResult";

export default {
  name: "MealView",
  components: {FoodListResult, FoodList, NutrientStats},
  data() {
    return {
      lmfs: [],
      lnf: [],
      meal: {},
      mealName: "",
      editMealNameMode: false,
      searchText: "",
      foods: []
    }
  },
  computed: {
    searchingFood() {
      console.log(this.$store.getters['layout/getMealViewTabSelected'] === 'Resultats')
      return this.$store.getters['layout/getMealViewTabSelected'] === 'Resultats'
    },
    canEdit() {
      if (this.authorId) {
        return localStorage.getItem("userId") === this.authorId.toString()
      }
      return undefined
    },
    author() {
      let userName = this.meal ? this.meal.username : ""
      if(userName.includes("@")){
        userName = userName.split("@")[0]
      } else if(userName.length>20){
        userName = userName.slice(0, 20) +"..."
      }
      return userName
    },
    authorId() {
      return this.meal ? this.meal.author_id : -1
    },
    searchMode() {
      return this.$store.getters['layout/getSearchMode']
    },
    mealViewTabSelected: {
      get() {
        return this.$store.getters['layout/getMealViewTabSelected']
      },
      set(val) {
        this.$store.commit('layout/updateMealViewTabSelected', val)
      }
    },
    from() {
      return this.$store.getters['layout/getFrom']
    },
    showArrowBack() {
      return this.from && this.from && this.from !== ""
    },
    largerThanSM() {
      return window.innerWidth > 1023
    },
    mealId() {
      return this.$route.params.id
    },

  },
  methods: {

    wantSearchFood() {
      this.$store.commit('layout/updateMealViewTabSelected', "Resultats")
      this.searchFoods()
    },
    editMealNameMode() {
      this.editMealNameMode = false
    },
    goBack() {
      this.$router.go(-1)
    },
    saveMealName() {
      this.$store.dispatch('meals/updateMeal', {id: this.mealId, name: this.mealName})
      this.editMealNameMode = false
    },
    searchFoods() {
      const callback = (data) => {
        propsToLowerCase(data);
        this.foods = data
      }
      const reqParamters = {
        "q": this.searchText.toLowerCase()
      }
      if (this.userIdParam) {
        reqParamters["userId"] = this.userIdParam
      }

      const url = "searchFoods"
      callGoApi(this, url, callback, reqParamters)
    },
    toggleSearchMode() {
      this.$store.commit('layout/updateSearchMode', true)
    },
    updateLinkMealFood(variables) {
      this.$store.dispatch('meals/updateLinkMealFood', variables)
      const {id: lmfId, conversionFactorId, quantity} = variables
      const lmfUpdatedIndex = this.lmfs.findIndex(e => e.id === lmfId)
      const lmfUpdated = this.lmfs[lmfUpdatedIndex]
      lmfUpdated.conversion_factor_id = conversionFactorId
      lmfUpdated.conversion_factor = lmfUpdated.conversionFactors.find(e => e.conversion_factor_id === conversionFactorId).conversion_factor
      lmfUpdated.quantity = quantity
      this.lmfs[lmfUpdatedIndex] = lmfUpdated
    },
    deleteLinkMealFoodList(lmfFoodIdDeleted) {
      const notDeleted = (id) => lmfFoodIdDeleted.indexOf(id) === -1
      const foodIdListDeleted = this.lmfs.filter(e => !notDeleted(e.id)).map(e => e.food_id)
      this.lmfs = this.lmfs.filter(e => notDeleted(e.id))
      this.lnf = this.lnf.filter(e => foodIdListDeleted.indexOf(e.food_id) === -1)

    },

    goTo(path) {
      this.$router.push({
        path: path
      })
    },

    fetchMealDatas() {
      const cpmt = this
      const mealid = this.$route.params.id
      this.$axios.get(`${process.env.GO_API_URL}/getMeal?mealId=` + mealid).then(response => {
        console.log(response.data[0])
        cpmt.meal = response.data[0]
        const mealList = []
        mealList.push(cpmt.meal)
        cpmt.$store.commit('meals/updateMealList', mealList)
        this.$store.commit('layout/updateHeaderTitle', cpmt.meal.name)
        this.mealName = cpmt.meal.name
      })

      this.$axios.get(`${process.env.GO_API_URL}/getLMF?mealId=` + mealid).then(response => {
        cpmt.lmfs = response.data
      })
      this.$axios.get(`${process.env.GO_API_URL}/getLNF?mealId=` + mealid).then(response => {
        cpmt.lnf = response.data
      })


    },
    deleteMeal() {
      const idList = []
      idList.push(this.meal.id)
      const payload = {idList: idList}
      const succesMessage = "Repas supprimmé avec succés"
      const callback = () => this.$router.push({path: "/"})
      sendForm(this, 'meals/deleteMeal', payload, succesMessage, callback)
    }
  },
  watch: {
    $route() {
      this.fetchMealDatas()
    },
    searchMode() {
      this.fetchMealDatas()
    },
    editMealNameMode() {
      if (this.editMealNameMode) {
        this.$refs.editMealNameInput.focus()
      }
    },
    searchText() {
      this.searchFoods()
    },
    mealViewTabSelected() {
      this.$refs.searchInput.focus()
    }
  },

  created() {
this.searchFoods()
    this.fetchMealDatas()
  },
  mounted() {

  }
}
</script>

