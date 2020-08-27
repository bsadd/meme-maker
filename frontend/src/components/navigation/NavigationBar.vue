<template>
    <div>
        <v-app-bar app>
            <template v-slot:img="{ props }">
                <v-img v-bind="props" src="../../assets/navbar_bg.gif" contain></v-img>
            </template>

            <v-row align="center">
                <v-col cols="2" md="3">
                    <router-link to="/" style="background: none">
                        <v-list-item class="px-0">
                            <v-list-item-title
                                class="white--text title font-weight-medium hidden-sm-and-down"
                            >MemesBD</v-list-item-title>
                        </v-list-item>
                    </router-link>
                </v-col>
                <v-col cols="8" md="5">
                    <search-bar></search-bar>
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="2" md="4">
                    <v-row class="hidden-sm-and-down" justify="end" align="center">
                        <div v-if="isLoggedIn">
                            <v-menu open-on-hover bottom left offset-y>
                                <template v-slot:activator="{ on }">
                                    <div v-on="on">
                                        <v-avatar
                                            size="30"
                                            color="accent"
                                            class="black--text"
                                            style="cursor: pointer"
                                        >{{ getInitials }}</v-avatar>

                                        <v-btn dark icon style="justify-content: start">
                                            <v-icon small>$vuetify.icons.caretDown</v-icon>
                                        </v-btn>
                                    </div>
                                </template>

                                <v-list>
                                    <v-list-item @click="visitProfile">
                                        <v-list-item-icon>
                                            <v-icon>$vuetify.icons.profile</v-icon>
                                        </v-list-item-icon>
                                        <v-list-item-content>
                                            <v-list-item-title>Your profile</v-list-item-title>
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item @click="logOut">
                                        <v-list-item-icon>
                                            <v-icon>$vuetify.icons.logout</v-icon>
                                        </v-list-item-icon>
                                        <v-list-item-content>
                                            <v-list-item-title>Log out</v-list-item-title>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list>
                            </v-menu>
                        </div>
                        <div v-else>
                            <router-link to="/login">Login</router-link>
                            <router-link to="/signup">Signup</router-link>
                        </div>
                    </v-row>
                    <v-row class="hidden-md-and-up" justify="end">
                        <v-app-bar-nav-icon style="color: white" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
                    </v-row>
                </v-col>
            </v-row>
        </v-app-bar>
        <mobile-hamburger-menu v-model="drawer"></mobile-hamburger-menu>
    </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    data() {
        return {
            drawer: false
        };
    },
    components: {
        "search-bar": () => import("./SearchBar"),
        "mobile-hamburger-menu": () => import("./MobileHamburgerMenu")
    },
    computed: {
        ...mapGetters("auth", ["isLoggedIn"]),
        ...mapGetters("profile", ["getInitials"])
    },
    methods: {
        visitProfile() {
            const uuid = this.$store.state.profile.uuid;
            this.$router.push({ name: "profile", params: { uuid } });
        },
        logOut() {
            this.$store.dispatch("auth/logOut");
            this.$router.push("/");
        }
    }
};
</script>

<style scoped>
a {
    color: white !important;
    background: linear-gradient(to bottom, white 0%, white 100%);
    background-position: left top;
    background-repeat: repeat-y;
    background-size: 2px 100%;
    transition: background-size 0.2s;
    margin: 0px 4px;
}

a:hover {
    font-weight: bolder;
    color: var(--v-primary-base) !important;
    background-size: 100% 100%;
}

.v-image >>> .v-image__image {
    background-repeat: repeat !important;
}

.v-list-item__icon {
    margin: 16px 0px !important;
}
</style>
