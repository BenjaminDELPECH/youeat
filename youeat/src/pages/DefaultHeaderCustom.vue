<template>
  <div class="flex  full-width"
       style="flex-flow:nowrap;"
       v-show="!searchMode"
       @click="toggleSearchMode"
  >
    <div style="display:flex;width:100%;" >
      <input type="search"
             v-model="searchText"
             style="width:100%;"
             placeholder="Rechercher..."
             id="searchInput"
             ref="searchInput"
             class="flex full-width searchBar q-pa-xs"

      />
    </div>
    <div class="q-ml-auto border1" style="border-left:none;">
      <q-btn
        flat
        icon="search"
      />
    </div>
  </div>
</template>
<script>
export default {
  name: 'DefaultHeaderCustom',
  methods: {
    toggleSearchMode() {
      this.$store.commit('layout/updateSearchMode', true)
    },
  },
  computed: {
    searchMode() {
      return this.$store.getters['layout/getSearchMode']
    },

  }
}
</script>
