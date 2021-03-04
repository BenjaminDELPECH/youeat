<template>

  <div class="full-width flex " style="">

<div class="no-wrap flex" style="width:100%;">
    <q-btn
      flat
      icon="arrow_back"
      @click="cancelSearch"
    />

    <div style="display:flex;width:100%;" class="q-pr-sm">
<!--      <input type="search"-->
<!--             style="width:100%;;"-->
<!--             placeholder="Rechercher..."-->
<!--             id="searchInput"-->
<!--             ref="searchInput"-->
<!--             class="flex full-width searchBar q-pl-md"-->

<!--      />-->
      <q-input label="search" dense v-model="searchText"
               style="width:100%;"
               type="search"  placeholder="Rechercher..."
               ref="searchInput"
        color="green"
      />
    </div>
</div>
    <div class="" style="width:100%;">
      <SearchResult :search-text="searchText"/>
    </div>
  </div>
</template>
<script>
import {DEFAULT_HEADER_TITLE_VAL, HEADER_ACTION_NORMAL} from "src/store/layout/state";
import SearchResult from "pages/SearchResult";

export default {
  name: 'HeaderCustom',
  components: {SearchResult},
  data() {
    return {
      wantSearchLocal: false,
      searchText: ""
    }
  },

  methods: {

    cancel() {
      this.searchText = ""
    },

    goBack() {
      this.wantSearchLocal = !this.wantSearchLocal
      this.searchText = ""
      this.$store.commit("layout/updateHeaderTitle", DEFAULT_HEADER_TITLE_VAL)
      this.$store.commit('layout/updateHeaderAction', HEADER_ACTION_NORMAL)
      this.$router.push({
        path: "/"
      })

    },

    cancelSearch() {
      this.$store.commit('layout/updateSearchMode', false)
    }
  },
  computed: {


    headerAction() {
      console.log(this.$store.getters['layout/getHeaderAction'])
      return this.$store.getters['layout/getHeaderAction']
    },
    isHeaderTitle() {
      return this.headerTitle !== DEFAULT_HEADER_TITLE_VAL
    },
    headerTitle() {
      return this.$store.getters['layout/getHeaderTitle']
    }
  },
  updated() {


    if (this.$refs.searchInput && this.wantSearchLocal) {
      this.$refs.searchInput.focus()
    }


  },
  mounted() {
    this.$refs.searchInput.focus()
  }


}
</script>
