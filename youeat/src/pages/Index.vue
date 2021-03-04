<template>
  <q-page>
    <div
      class="flex  full-width q-mb-sm q-pb-sm q-pt-sm q-pr-sm borderBottom1" bordered
      style="flex-flow:nowrap;">
      <div class="q-ml-auto">
        <q-btn
          @click="toggleSearchMode"
          flat
          class="q-ml-auto"

          icon="search"
        />
      </div>
    </div>


    This is index

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="accent" @click="createMeal"/>
    </q-page-sticky>

  </q-page>
</template>

<script>
import CustomCard1 from "pages/MealCard";
import SearchResult from "pages/SearchResult";

export default {
  name: 'PageIndex',
  components: {CustomCard1, SearchResult},
  data() {
    return {
      value: 33,

    }
  },

  methods: {
    toggleSearchMode(){
      this.$store.commit('layout/updateSearchMode', true)
    },
    goTo(path) {
      this.$router.push({
        path: path
      })
    },

    createMeal() {

    },
  },
  created() {
    // this.$store.commit('layout/updateSearchMode', true)
  }
}
</script>
