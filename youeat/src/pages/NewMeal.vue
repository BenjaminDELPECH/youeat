<template>
  <div>
    <div class="flex  full-width q-mb-sm q-pb-sm q-pt-sm q-pr-sm" bordered
         style="flex-flow:nowrap;">


      <div class="">
        <q-btn
          flat
          icon="arrow_back"

          @click="goBack()"
        />

      </div>
      <div style="margin:auto 0;" class="q-pl-md">

        Nouveau repas
      </div>


      <q-btn
        @click="goTo('/search')"
        flat
        class="q-ml-auto"

        icon="search"
      />


    </div>


    <q-card bordered flat class="q-ma-md">


      <q-form class="q-gutter-md"
              @submit="submit"

      >
        <q-card-section>

          <q-input label="Nom du repas" type="text" v-model="mealName"/>


        </q-card-section>
        <q-card-section>
          <q-btn label="Valider" type="submit" color="primary"/>
        </q-card-section>
      </q-form>
    </q-card>
  </div>
</template>

<script>
import {sendForm} from "src/utils/sendForm";

const successMessage = "Repas créé avec succès";

export default {
  name: "NewMeal",
  data() {
    return {
      mealName: ""
    }
  },
  methods: {
    goBack() {
      history.back()
    },
    redirectToMeals() {
      this.$router.push({
        path: '/myMeals'
      })
      this.$router.reload()
    },
    goTo(path) {
      this.$router.push({
        path: path
      })
    },
    submit() {
      const payload = {"name": this.mealName}
      sendForm(this, 'meals/createMeal', payload, successMessage, this.redirectToMeals)
    }
  },
  computed: {
    userId() {
      return this.$store.getters['user/getUser'].id
    }
  }
}
</script>

<style scoped>

</style>
