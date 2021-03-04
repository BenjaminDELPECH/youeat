<template>
  <q-dialog v-model="showAuthProxy">


    <q-card v-show="dialogAction==='signIn'">
      <q-card-section class="bg-primary text-white">
        <div class="text-h6">Connectez-vous !</div>
      </q-card-section>
      <q-card-section>
        <q-form class="q-gutter-md">
          <q-input label="email" name="email" :value="email"/>
          <q-input type="password" label="Mot de passe" name="password" :value="email"/>
          <q-toggle v-model="accept" label="J'accepte les termes et conditions"/>
          <div>
            <q-btn label="Valider" type="submit" color="primary"/>
          </div>
        </q-form>
      </q-card-section>
    </q-card>


    <q-card v-show="dialogAction==='signUp'">
      <q-card-section>
        Sign up
      </q-card-section>
    </q-card>

  </q-dialog>
</template>
<script>
export default {
  name: 'DialogCustom',
  data() {
    return {
      email: "",
      password: "",
      accept: false
    }
  },
  props: {
    dialogAction: {}
  },
  computed: {
    showAuthProxy: {
      get() {
        return this.dialogAction !== -1
      },
      set() {
        this.$store.commit('layout/updateDialogAction', -1)
      }
    }
  }
}
</script>
