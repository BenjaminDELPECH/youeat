<template>
  <q-page class="q-pa-md container2" style="">
    <q-card bordered flat class="shadow-custom1">
      <q-card-section>
        <div class="text-h6">Récupération de mot de passe</div>
      </q-card-section>
      <q-card-section v-show="errors.length>0">
        <div class="bg-red text-white q-pa-sm" v-for="error in errors">
          {{ error }}
        </div>
      </q-card-section>

      <q-card-section>

        <!--        //-->
        <q-form class="q-gutter-md"
                v-if="!codeValidated">
          <q-input filled
                   color="positive"
                   label-color="positive"
                   label="email" type="email" name="email"
                   v-model="email"/>
          <q-btn label="Envoyer" flat  class="border1" @click="sendActivationCode"/>
        </q-form>

        <!--        //-->
        <q-form v-if="mailSended">
          <q-input
            filled
            label="Code"
            abel-color="positive"
            type="number"
            name="code"
            v-model="code"
          />
          <q-btn label="Valider" flat  class="border1" @click="validateCode"/>
        </q-form>

        <!--        //-->
        <q-form class="q-gutter-md"
                v-if="codeValidated">
          <q-input filled label-color="positive" color="positive" type="password" label="Nouveau mot de passe"
                   name="password"
                   v-model="newPassword"
                   :rules="[
          validatePassword
        ]"
          />
          <q-input filled label-color="positive" color="positive" type="password"
                   label="Confirmation de mot de passe"
                   v-model="secondPassword"
          />
           <q-btn label="Valider" flat  class="border1" @click="changePassword"/>
        </q-form>
      </q-card-section>
      <q-card-section>
        <span class="text-caption">
          youeat.fr va vous envoyé un code de vérification par mail.
        </span>
      </q-card-section>
      <q-card-section>
        <div>

        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import {validatePassword} from "src/utils/utils";

export default {
  name: "ForgotPassword",
  data() {
    return {
      email: "",
      mailSended: false,
      code: undefined,
      errors: [],
      codeValidated: false,
      newPassword: "",
      secondPassword: ""
    }
  },
  methods: {
    manageErrros: function (error, cpmt) {
      const backendErrors = error.graphQLErrors.map(e => e.message)
      cpmt.errors = cpmt.errors.concat(backendErrors)
    },
    sendActivationCode() {
      const cpmt = this
      const payload = {"email": this.email}
      this.$store.dispatch('user/sendVerificationCodeMail', payload).then(response => {
        console.log(response)
        const {sendVerificationCodeMail} = response
        const {mailSended} = sendVerificationCodeMail
        cpmt.mailSended = mailSended
      }).catch(error => {
        this.manageErrros(error, cpmt);
      })
    },
    validateCode() {
      const cpmt = this
      this.$store.dispatch('user/verifyCode', {"code": this.code, "email": this.email}).then(response => {
        const {verifyCode} = response
        const {success} = verifyCode
        if (success) {
          cpmt.codeValidated = true
          cpmt.codeValidated = true
        }
      }).catch(error => {
        this.manageErrros(error, cpmt);
      })
    },
    changePassword(){
      const cpmt = this
      const payload = {
        "email": this.email,
        "newPassword": this.newPassword}
        console.log(payload)
      this.$store.dispatch('user/changePassword', payload).then(response=>{
        console.log(response)
        const {changePassword} = response
        const {token, userId} = changePassword
        if(token){
          localStorage.setItem('token', token)
          localStorage.setItem('userId', userId)
          this.$router.push({
            path: '/'
          })
          this.$router.go()
        }
      }).catch(error=>{
        this.manageErrros(error, cpmt);
      })
    },
      validatePassword(val) {
      var passw = /^[A-Za-z]\w{7,100}$/;
      if (val.match(passw)) {
        return true;
      } else {
        return "Entrez un mot de passe entre 6 et 100 caractères, qui contient au moins un caractère numérique";
      }
    },
  }
}
</script>

<style scoped>

</style>
