<template>
  <div class="q-pb-xl">
    <div v-for="food in foods" class="flex q-pa-xs "

         style="flex-flow: nowrap;width:100%;">
      <div class="" style="">
        <q-btn name="" label="+"
               @click="addFood(food)"
               size="sm"
               flat
               class="border1"
               v-show="mealIdSelected!==-1"
        />
      </div>
      <div class="flex q-pl-sm">
        <div class="link1" style="margin:auto;"
             @click="goToObjId('/food',food.id)">{{ food.namefr }}</div>
      </div>
      <div class="flex q-pl-sm q-ml-auto tooltip">
        <q-icon
          title="Hello"
          size="xs" name="done"  style="margin:auto;"
          v-if="food.convfactornb > 2"


        />
        <span class="tooltiptext" >Aliment confirmé</span>
      </div>

    </div>
  </div>
</template>
<script>
import {addFood} from "src/utils/food";

export default {
  name: 'FoodListResult',
  props: {
    mealIdSelected: {},
    foods: {}
  },
  methods: {
    addFood(food) {
      addFood(this, food, this.mealIdSelected)
    },
    goToObjId(path, id) {
      this.$router.push({
        path: path + "/" + id,

      })
    },
  },
  created() {
  }
}
</script>
<style scoped>

@media screen and (max-width: 800px) {
}

@media screen and (max-width: 450px) {
}
</style>
