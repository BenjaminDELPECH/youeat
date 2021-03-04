<template>
  <q-layout view="lhh LpR lff" container style="height:100vh" class="shadow-2 rounded-borders">
    <q-header  class="full-width" id="header" style="background-color:unset;position:absolute;width:100%;" v-show="searchMode">

        <HeaderCustom/>

    </q-header>

    <q-footer
      id="footer"
      v-if="token"
      class="flex  "
      style=""
    >
      <q-card class="flex q-pa-sm sm-larger-hide" flat square dark
              style="width:100%;justify-content: space-around;">
        <div v-for="elem in linksData" @click="goTo(elem.link)" class="flex" style="width:33%;">

          <div class="flex" style="margin:auto;flex-direction: column">
            <q-icon :name="elem.icon" size="sm" style="margin:auto;"/>
            <div v-show="routePath===elem.link">
              {{ elem.title }}
            </div>

          </div>
        </div>
      </q-card>
    </q-footer>
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class=""
    >
      <q-list>
        <q-item-label
          header
          class="text-grey-8"
        >
          <!--          Essential Links-->
        </q-item-label>
        <EssentialLink
          v-for="link in linksData"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>
    <q-page-container :style="mainStyle">
      <router-view/>
    </q-page-container>
    <DialogCustom :dialogAction="dialogAction"/>

  </q-layout>
</template>

<script>
import EssentialLink from 'components/EssentialLink.vue'
import HeaderCustom from "layouts/HeaderCustom";
import {DEFAULT_HEADER_TITLE_VAL, HEADER_ACTION_NORMAL} from "src/store/layout/state";
import DialogCustom from "layouts/DialogCustom";
import {getTokenFromLocalStorage} from "src/utils/commonUtils";
import {callGoApi} from "src/utils/api";
import {getCalory} from "src/utils/calories";


export default {
  name: 'MainLayout',
  components: {DialogCustom, HeaderCustom, EssentialLink},
  data() {
    return {
      leftDrawerOpen: false,
    }
  },
  computed: {
    token() {
      return this.$store.getters['user/getToken']
    },
    mainStyle() {
      return "padding-bottom:0"+ (this.searchMode ? "opacity: 0" : "")
    },
    searchMode() {
      console.log(this.$store.getters['layout/getSearchMode'])
      return this.$store.getters['layout/getSearchMode']
    },
    routePath() {
      return this.$route.path
    },
    showHeader() {
      const path = this.$route.path
      return false

    },
    userId() {
      return localStorage.getItem('userId')
    },
    linksData() {
      const baseUlrs = [
        //   {
        //   title: 'Acceuil',
        //   caption: '',
        //   icon: 'home',
        //   link: '/'
        // }
      ]
      // baseUlrs.push({
      //   title: 'Home',
      //   caption: '',
      //   icon: 'home',
      //   link: '/'
      // });
      if (getTokenFromLocalStorage()) {
        baseUlrs.push({
          title: 'Mes repas',
          caption: '',
          icon: 'local_dining',
          link: '/myMeals'
        });
        baseUlrs.push({
          title: 'Profil',
          caption: '',
          icon: 'account_circle',
          link: '/profil'
        })
      } else {


        baseUlrs.push({
          title: "Authentification",
          caption: '',
          icon: 'account_box',
          link: '/signIn'
        });
      }
      return baseUlrs

    },
    dialogAction() {
      return this.$store.getters['layout/getDialogAction']
    },


    isHeaderTitle() {
      return this.headerTitle !== DEFAULT_HEADER_TITLE_VAL
    },
    headerTitle() {
      return this.$store.getters['layout/getHeaderTitle']
    },
    isHeaderActionNormal() {
      return this.headerAction === HEADER_ACTION_NORMAL
    },
    headerAction() {
      return this.$store.getters['layout/getHeaderAction']
    }
  },
  methods: {
    goTo(path) {
      this.$router.push({
        path: path
      })
    },
    handleProfileResponse: function (response) {
      this.$store.commit('user/setProfile', response[0])
      this.$store.commit('user/updateCaloriesNeed', getCalory(response[0]))
    },

  },
  watch: {
    $route(newVal, old) {
      this.$store.commit('layout/updateFrom', old.path)
      this.$store.commit('layout/updateSearchMode', false)
      if (old.path.includes("activate")) {
        this.$router.go()
      }
    },
    userId() {
      const cpmt = this
      if (this.userId) {
        callGoApi(this, '/getProfile', (response) => {
          cpmt.$store.commit('user/setProfile', response[0])
          cpmt.$store.commit('user/updateCaloriesNeed', getCalory(response[0]))
        }, parameters)
      }
    },
  },


  created() {

    this.$axios.get(`${process.env.GO_API_URL}/getNutrientGroups`).then(response => {
      this.$store.commit('nutrients/updateNutrientGrps', response.data)
    })
    this.$axios.get(`${process.env.GO_API_URL}/getNutrients`).then(response => {

      this.$store.commit('nutrients/updateNutrients', response.data)
    })
  const cpmt = this
    if (this.userId) {
      let parameters = {"user_id": localStorage.getItem("userId")}
      callGoApi(this, '/getProfile', (response) => {
         cpmt.$store.commit('user/setProfile', response[0])
          cpmt.$store.commit('user/updateCaloriesNeed', getCalory(response[0]))
      }, parameters)

      this.$store.dispatch('user/getUser')
    }
  },

}
</script>
