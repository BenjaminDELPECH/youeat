<template>
  <div style="width:100%;overflow:auto;">
    <div v-show="!searchMode" class="q-mt-xs" style="">
      <q-btn label="Nouveau repas"
             @click="createMeal"
             flat
             class="border1"
      />
    </div>
    <div style="width:100%;display:flex;flex-flow: wrap;">
      <div v-for="elem in meals"
           class="meal-result-container"
      >
        <q-card class="flex border1 selectable q-mt-xs q-mr-sm" flat @click="goToMeal(elem)">
          <CustomCard1 :name="elem.name" :calorie="elem.calorie"/>
        </q-card>
      </div>
    </div>
  </div>
</template>
<script>
import CustomCard1 from "pages/MealCard"

export default {
  name: 'SearchResultContent',
  components: {CustomCard1},
  props: {
    meals: {}
  },
  computed: {
    searchMode() {
      return this.$store.getters['layout/getSearchMode']
    }
  },
  methods: {
    createMeal() {
      this.$router.push({
        path: '/newMeal'
      })
    },
    goToMeal(meal) {
      const {id, name} = meal
      this.$router.push({
        path: '/meal/' + id
      })
      this.$store.commit('layout/updateHeaderTitle', name)
      this.$store.commit('layout/updateSearchMode', false)

    }
  },
  created() {

  }
}
</script>
<style scoped>
.meal-result-container {
  width: 33%;
}

@media screen and (max-width: 800px) {
  .meal-result-container {
    width: 50%;
  }
}

@media screen and (max-width: 450px) {
  .meal-result-container {
    width: 100%;
  }
}
</style>
