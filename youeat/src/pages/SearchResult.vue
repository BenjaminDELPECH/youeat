<template>
  <div class=" " style="width:100%;">

    <div id="searchTabs" style="max-width: 100%;">
      <q-tabs

        v-model="objectTypeProxy"
        inline-label
        outside-arrows
        mobile-arrows
        dense
      >
        <div class="flex q-mr-auto">
          <q-tab name="meal"  label="Repas"  />
          <q-tab name="food"  label="Aliments"/>
        </div>
      </q-tabs>

    </div>
    <div class="">
      <div v-show="objectTypeProxy==='meal'" class="q-pt-sm" :style="resultStyle">
        <SearchResultContent :meals="meals"/>
        <div class="q-pa-md" v-show="!meals.length">
          0 résultat pour "{{ this.searchText }}"
        </div>
      </div>

      <div v-show="objectTypeProxy==='food'" class="flex" :style="resultStyle">
        <div v-if="mealSelected && mealSelected.name" class="q-ml-auto q-mr-sm q-mt-sm">
          <q-badge transparent color="" class="q-pa-sm mt-sm" @click="goToMeal(mealIdSelected)">
            {{ mealSelected.name }}
          </q-badge>
        </div>

        <FoodListResult
                        :foods="foods"
                        :meal-id-selected="mealIdSelected"

        />

      </div>
    </div>
  </div>
</template>

<script>
import {callGoApi, propsToLowerCase} from "src/utils/api";
import SearchResultContent from "pages/SearchResultContent";
import {addFood} from "src/utils/food";
import FoodListResult from "pages/FoodListResult";


export default {
  name: "SearchResult",
  components: {FoodListResult, SearchResultContent},
  props: ['searchText'],
  data() {
    return {
      meals: [],
      foods: [],
      shape: 'Tout',
      objectType: "meal",
      tab: "test",
      maxResultHeightPx: -1
    }
  },
  methods: {

    goToMeal(mealIdSelected) {
      this.$store.commit('layout/updateSearchMode', false)
      const path = "/meal/" + mealIdSelected
      this.goTo(path)
    },
    goTo(path) {
      this.$router.push({
        path: path
      })
    },
    createMeal() {
      if (localStorage.getItem('token')) {
        this.goTo('newMeal')
      } else {
        this.goTo('signIn')
      }
    },

    searchMeals: function () {
      const callback = (data) => {
        if (data) {
          propsToLowerCase(data);
          this.meals = data
        } else {
          this.meals = []
        }
      }
      const reqParamters = {
        "q": this.searchText
      }
      console.log(this.userIdParam)
      if (this.userIdParam) {
        reqParamters["userId"] = this.userIdParam
      }

      const url = "searchMeals"
      callGoApi(this, url, callback, reqParamters);
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

    search: function () {


      const footerHeight = document.getElementById("footer").offsetHeight
      const headerHeight = document.getElementById("header").offsetHeight
      const tabHeight = document.getElementById("searchTabs").offsetHeight
      const othersElemesHeightPx = headerHeight + footerHeight + tabHeight
      this.maxResultHeightPx = window.innerHeight - othersElemesHeightPx

      this.searchMeals();
      this.searchFoods();

    },
    cancel() {
      this.searchText = ""
    },
    goBack() {
      history.back()
    },
    fetchMeals() {

      const parameters = {"userId": this.userId}
      const cpmt = this
      callGoApi(this, 'meals', (data) => {
        if (cpmt.user && cpmt.user.id) {
          cpmt.myMeals = data.filter(e => e.author_id === cpmt.user.id)
        }
        cpmt.$store.commit('meals/updateMealList', cpmt.myMeals)
        cpmt.fetched = true
      }, parameters)
    },

  },
  computed: {
    user() {
      return this.$store.getters['user/getUser']
    },
    userId() {
      return this.user.id
    },
    resultStyle() {
      return "overflow:auto ;max-height : " + this.maxResultHeightPx + "px"
    },
    showArrowBack() {
      return this.$route.path !== '/'
    },
    mealList() {
      return this.$store.getters['meals/getMealList']
    },
    mealSelected() {
      if (this.mealList && this.mealList.length && this.mealList[0] !== undefined) {
        return this.mealList.find(e => e.id === this.mealIdSelected)
      }
    },
    mealIdSelected() {
      return this.$store.getters['layout/getMealIdSelected']
    },
    objectTypeProxy: {
      get() {
        return this.$store.getters['layout/getSearchPageTabSelected']
      },
      set(newVal) {
        this.$store.commit('layout/updateSearchPageTabSelected', newVal)
      }
    },
    q() {
      return this.$route.query.q
    },
    userIdParam() {
      return this.$route.query.userId
    }
  }
  ,
  watch: {
    searchText(newVal, oldVal) {
      this.search();
    }
  }
  ,
  mounted() {
    this.search()
    if (this.userId) {
      this.fetchMeals()
    }

  },

}
</script>

<style scoped>

@media screen and (max-width: 800px) {
}

@media screen and (max-width: 450px) {
}
</style>
