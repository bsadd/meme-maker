<template>
    <v-row>
        <v-col cols="12" sm="3">
            <ad-section></ad-section>
        </v-col>
    </v-row>
</template>

<script>
export default {
  components: {
    'ad-section': () => import('../components/search/AdSection')
  }
}
</script>

<style>

</style>