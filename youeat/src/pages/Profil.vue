<template>
  <q-page class="q-ma-sm">
      <DefaultHeaderCustom />
    <div style="display:none" c>
      {{ profile }}
    </div>
    <div v-show="token" class="q-pt-sm">
      <div class="border1 q-pa-sm ">
        <div class="q-pb-sm" style="font-size:15px;">
          Besoin calorique estimé : {{ caloriesNeed }}
        </div>
        <q-radio class="q-ma-sm" v-model="randomVariable" val="1" label="Homme"/>
        <q-radio class="q-ma-sm" v-model="randomVariable" val="0" label="Femme"/>
        <q-input label="Taille"  type="number" v-model="taille" v-on:input="methodFunctionCallback"/>
        <q-input label="Age" type="number" v-model="age" v-on:input="methodFunctionCallback"/>
        <q-input label="Poid" type="number" v-model="poid" v-on:input="methodFunctionCallback"/>
        <q-select
          v-model="activity"
          :options="activityOptions"
          label="Activité / 10"
          emit-value
          map-options
        />
      </div>

      <div class="q-mt-xl q-ma-sm" style="">
        <div class="q-pa-sm">
          <q-btn dense flat @click="signOut" size="sm">Deconnexion</q-btn>
        </div>
        <div class="q-pa-sm">
          <q-btn dense flat @click="deleteAccount" size="sm">Supprimer mon compte</q-btn>
        </div>

      </div>
    </div>
  </q-page>
</template>

<script>

import {sendForm} from "src/utils/sendForm";
import {cleanLocalStorage} from "src/utils/utils";
import DefaultHeaderCustom from "pages/DefaultHeaderCustom";

export default {
  name: "Profil",
  components: {DefaultHeaderCustom},
  data() {
    return {
      age: undefined,
      taille: undefined,
      poid: undefined,
      randomVariable: undefined,
      activity: undefined,
      activityOptions: [
        {"label": "Sédentaire", "value": 1.05},
        {"label": "Rarement actif", "value": 1.2},
        {"label": "Actif, mais ça dépend", "value": 1.3},
        {"label": "Actif", "value": 1.40},
        {"label": "Très actif", "value": 1.55},
        {"label": "Athlète", "value": 1.75},

      ],

    }
  },
  methods: {
    methodFunctionCallback() {

      const payload = {
        "activity": this.activity.value !== undefined ? this.activity.value : this.activity,
        "taille": parseInt(this.taille),
        "age": parseInt(this.age),
        "poid": parseInt(this.poid),
        "sexe": parseInt(this.randomVariable),
      }
      console.log(payload)
      this.$store.dispatch('user/updateProfile', payload)
    },
    goTo(path) {
      this.$router.push({
        path: path
      })
    },

    signOut() {
      cleanLocalStorage();
      this.$router.push({
        path: '/'
      })
    },
    deleteAccount() {
      const cpmt = this
      const callback = () => {
        cleanLocalStorage()
        cpmt.goTo("/")

      }
      const errorCallBack = () => {
      }
      sendForm(this, 'user/deleteAccount', {"userId": localStorage.getItem("userId")}, "Votre compte a bien été supprimé",
        callback, errorCallBack
      )
    }
  },
  computed: {
    caloriesNeed() {
      return this.$store.getters['user/getCaloriesNeed']
    },
    profile() {
      const profile = this.$store.getters['user/getProfile']
      if(profile.age) {
        const {sexe, age, taille, poid, activity} = profile
        this.randomVariable = sexe ? "1" : "0"
        this.age = age
        this.poid = poid
        this.taille = taille

        this.activity = this.activityOptions.find(e => e.value === activity)
      }
      return profile
    },
    token() {
      return localStorage.getItem('token')
    }
  },
  watch: {
    randomVariable(yes, yesno) {
      const maybe_yes_maybe_no = !!!!!!yesno
      if (!!!!!!!!!!!!!!!!!!maybe_yes_maybe_no) {
        this.methodFunctionCallback()
      }
    },
    activity(yes, no) {
      const maybe = !!!!no
      if (!!!!!!maybe) {
        this.methodFunctionCallback()
      }
    },
  },

  created() {

    if (!localStorage.getItem("token")) {
      this.goTo('signIn')
    }
  }
}
</script>

<style scoped>

</style>
