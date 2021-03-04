<template>
  <div>
    salue
    {{ params }}
  </div>
</template>

<script>
import {setCookie} from "src/utils/cookieUtils";

export default {
  name: "Activate",
  computed: {
    params() {
      return this.$route.query
    },
    token() {
      return localStorage.getItem("token")
    }
  },
  created() {
    if (!this.token) {
      const cpmt = this
      const {activation_token, token} = this.$route.query

      this.$store.dispatch('user/activateUser', {"activationToken": activation_token}).then(response => {
        console.log(response)

        const {activateUser} = response
        const {userId} = activateUser
        localStorage.setItem('userId', userId)
        localStorage.setItem('token', token)

        this.$store.commit('user/setToken', token)

        this.$router.push({
          path: '/myMeals'
        })

      }).catch(err => {
        console.log(err)
        // cpmt.$router.push({
        //   path: "/"
        // })
      })


      this.$q.notify('Compte validé ! Vous etes connecté !')
    }
  }
}
</script>

<style scoped>

</style>
