<template>
    <v-row style="height: 100%">
        <v-col cols="12" md="7" style="height: 100%;">
            <router-view></router-view>
        </v-col>
    </v-row>
</template>

<script>
export default {};
</script>

<style scoped>
#welcome-card {
    border-radius: 0px !important;
    padding: 50px;
}
</style>