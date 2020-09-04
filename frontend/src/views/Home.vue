<template>
    <v-row>
        <v-col cols="3" class="hidden-sm-and-down">
            <side-panel></side-panel>
        </v-col>
        <v-col cols="12" sm="9" md="6">
            <post-list></post-list>
        </v-col>
        <v-col cols="12" sm="3">
            <ad-section></ad-section>
        </v-col>
        <v-btn fixed fab bottom right color="primary" @click.native="scrollToTop">
            <v-icon>$vuetify.icons.arrowUp</v-icon>
        </v-btn>
    </v-row>
</template>

<script>
export default {
    components: {
        "side-panel": () => import("@/components/home/SidePanel"),
        "post-list": () => import("@/components/search/NewsFeed"),
        "ad-section": () => import("../components/search/AdSection")
    },
    methods: {
        scrollToTop() {
            window.scrollTo(0, 0);
        }
    }
};
</script>

<style>
</style>