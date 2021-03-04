<template>
 <q-dialog v-model="confirm" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar :icon="iconName" color="primary" text-color="white" />
          <span class="q-ml-sm">{{label}}</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="primary" v-close-popup @click="cancelAction" />
          <q-btn flat label="Confirmer" color="primary" v-close-popup @click="confirmAction" />
        </q-card-actions>
      </q-card>
    </q-dialog>
</template>

<script>
export default {
  name: "ConfirmDialog",
  props:['show', 'iconName', 'label','confirmAction','cancelAction'],
  data(){
    return{
      confirm:true
    }
  }
}
</script>

<style scoped>

</style>
