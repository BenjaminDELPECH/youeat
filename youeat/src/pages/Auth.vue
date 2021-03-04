<template>
  <q-page class="q-pa-md container2" style="">
    <q-card bordered flat class="shadow-custom1">
      <q-card-section>
        <div class="text-h6">{{ title }}</div>
      </q-card-section>
      <q-card-section v-show="errors.length>0">
        <div class="bg-red text-white q-pa-sm" v-for="error in errors">
          {{ error }}
        </div>
      </q-card-section>
      <q-card-section>
        <q-form class="q-gutter-md"

        >

          <q-input filled v-show="isSignIn"
                   color="positive"
                   label-color="positive"
                   label="email"
                   type="email"
                   name="email"
                   v-model="email"/>


        <q-input
          color="positive"
          label-color="positive"
          v-show="!isSignIn"
          label="email"
          type="email"
          name="email"
          v-model="email"
          filled
          :rules="[validateEmail]"
        />

      <q-input filled v-show="isSignIn" label-color="positive" color="positive" type="password" label="Mot de passe"
               name="password"
               v-model="password"/>
      <q-input filled v-show="!isSignIn" label-color="positive" color="positive" type="password" label="Mot de passe"
               name="password"
               v-model="password"
               :rules="[
          validatePassword
        ]"
      />
      <q-input filled v-show="!isSignIn" label-color="positive" color="positive" type="password"
               label="Confirmation de mot de passe"
               v-model="secondPassword"
               :rules="[
          validatePassword
        ]"
      />

      <q-toggle v-show="!isSignIn" v-model="accept" label="J'accepte les termes et conditions"/>
      <div>
        <q-btn label="Valider" flat type="submit" class="border1" @click="sign" v-show="isSignIn" />
        <q-btn label="Valider" flat type="submit" class="border1"   v-show="!isSignIn" />
      </div>
      </q-form>
      </q-card-section>
      <q-separator/>
      <q-card-section>
        <div class="text-subtitle2">
          <div v-if="isSignIn" class="borderTop q-pt-sm q-pb-sm selectable" @click="goTo('/signUp')">M'inscrire</div>
          <div v-if="!isSignIn" class="borderTop q-pt-sm q-pb-sm selectable" @click="goTo('/signIn')">Me connecter</div>
          <div v-if="isSignIn" class="borderTop q-pt-sm q-pb-sm selectable" @click="goTo('/forgotPassword')">J'ai oublié
            mon mot de passe
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>

import {sendForm} from "src/utils/sendForm";
import {getCookie} from "src/utils/cookieUtils";
import {signIn} from "src/utils/auth";
import {validatePassword} from "src/utils/utils";

const successMessage = "Un mail vous a été envoyé pour confirmer votre inscription"

export default {
  name: "SignIn",
  data() {
    return {
      email: "",
      password: "",
      secondPassword: "",
      accept: false,
      errors: []
    }
  },
  props: {
    dialogAction: {}
  },
  computed: {
    currentPath() {
      return this.$route.path
    },
    isSignIn() {
      return this.$route.path === '/signIn'
    },
    title() {
      return this.isSignIn ? "Connectez-vous" : "Inscrivez-vous"
    }
  },
  methods: {

    goTo(path) {
      this.$router.push({
        path: path
      })
    },
    validateEmail(val) {
      if (/^\w+([\.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(val)) {
        return true
      }
      return "Veillez entrer une adresse mail valide"
    },
    validatePassword(val) {
      var passw = /^[A-Za-z]\w{7,100}$/;
      if (val.match(passw)) {
        return true;
      } else {
        return "Entrez un mot de passe entre 6 et 100 caractères, qui contient au moins un caractère numérique";
      }
    },
    signUp: function () {
      if (this.password !== this.secondPassword) {
        this.errors.push("Les deux mots de passes doivent etre identiques")
        return
      }
      this.errors = []
      if (this.accept !== true) {
        this.errors.push(
          'You need to accept the license and terms first'
        )
      } else {
        //
        const payload = {
          "email": this.email,
          "password": this.password,
          "anonymousUserId": parseInt(getCookie('anonymousUserId'))
        }

        let successMessage = 'Un email de confirmation vous a été envoyé'
        const cpmt = this
        sendForm(this, 'user/createUser', payload, successMessage,
          () => {

          },
          error => {
            const {graphQLErrors} = error
            const backendErrors = error.graphQLErrors.map(e => e.message)
            cpmt.errors = cpmt.errors.concat(backendErrors)
          })

      }
    },

    sign() {
      if (!this.isSignIn) {
        this.signUp();
      } else {
        const paylad = {"email": this.email, "password": this.password}
        const callback = () => {
          this.$router.push({
            path: '/'
          })
          this.$router.go()

        }

        sendForm(this, 'user/login', paylad, "Vous etes connecté !", callback)
      }

    },
  }
}
</script>

<style scoped>

</style>
