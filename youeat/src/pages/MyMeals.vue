<template>
  <q-page class="flex q-ma-xs">
    <div v-show="token" class="full-width">
      <DefaultHeaderCustom/>
      <SearchResultContent :meals="myMealsProxy" v-show="!searchMode"/>
    </div>


  </q-page>
</template>

<script>
import {callGoApi} from "src/utils/api";
import SearchResultContent from "pages/SearchResultContent";
import DefaultHeaderCustom from "pages/DefaultHeaderCustom";

export default {
  name: "MyMeals",
  components: {DefaultHeaderCustom, SearchResultContent},
  data() {
    return {
      myMeals: [],
      fetched: false
    }
  },
  computed: {
    searchMode() {
      return this.$store.getters['layout/getSearchMode']
    },
    token() {
      return localStorage.getItem('token')
    },
    myMealsProxy: {
      get() {
        if (!this.myMeals.length && !this.fetched && this.user && this.user.id) {
          this.fetchMeals()
        } else {
          return this.myMeals
        }
      },
    },
    user() {
      return this.$store.getters['user/getUser']
    }
  },
  methods: {
    goBack() {
      history.back()
    },


    goTo(path) {
      this.$router.push({
        path: path
      })
    },


    fetchMeals() {
      const userId = parseInt(this.user.id)
      const parameters = {"userId": userId}
      const cpmt = this
      callGoApi(this, 'meals', (data) => {
        cpmt.myMeals = data.filter(e => e.author_id === userId)
        cpmt.$store.commit('meals/updateMealList', cpmt.myMeals)
        cpmt.fetched = true
      }, parameters)
    },
  },
  watch: {
    user() {
      if (this.user && this.user.id) this.fetchMeals()
    }
  },
  created() {

    this.$store.commit('layout/updateHeaderTitle', "Mes Repas")
    if (!localStorage.getItem("token")) {
      this.goTo('signIn')
    } else if (this.user && this.user.id) {
      this.fetchMeals()
    }
  }

}
</script>

