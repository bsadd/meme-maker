<template>
    <v-app>
        <initial-loading v-if="loading"></initial-loading>
        <v-content v-else>
            <navigation-bar></navigation-bar>
            <router-view></router-view>
        </v-content>
    </v-app>
</template>

<script>
import NavigationBar from "@/components/navigation/NavigationBar";
import InitialLoading from "@/components/loading/InitialLoading";

export default {
    name: "App",
    components: {
        InitialLoading,
        NavigationBar
    },
    data() {
        return {
            loading: true
        };
    },
    created() {
        this.$store
            .dispatch("auth/autoLogin")
            .then(() => this.$store.dispatch("profile/fetchCurrentUserProfile"))
            .finally(() => setTimeout(() => (this.loading = false), 1000));
    }
};
</script>

<style>
a {
    text-decoration: none;
    padding: 0px 16px;
    font-weight: normal;
}

.v-btn {
    text-transform: none;
}

.v-card {
    border-radius: 10px !important;
}

.v-card,
.v-card__title,
.v-card__subtitle,
.v-card__text {
    word-break: normal !important;
}

.v-subheader {
    padding: 0px !important;
    height: 24px !important;
}

.v-input input {
    color: black !important;
}

.v-icon {
    font-size: 16px !important;
    margin-top: 0px !important;
}

.v-select__selection {
    padding-left: 5px;
    max-width: 100%;
}

.v-select__selections input {
    width: 0px;
}

.v-banner__content {
    justify-content: center !important;
}

.loading-btn {
    padding: 0px !important;
}

.loading-btn .v-btn__content {
    height: 100% !important;
}
</style>