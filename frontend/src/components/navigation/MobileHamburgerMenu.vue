<template>
    <v-navigation-drawer
        v-if="$vuetify.breakpoint.name === 'sm' || $vuetify.breakpoint.name === 'xs'"
        v-model="drawer"
        left
        app
    >
        <v-list>
            <v-list-item style="padding: 16px 32px">
                <v-list-item-avatar>
                    <img src="@/assets/doge.png" alt="buet-logo" />
                </v-list-item-avatar>
                <v-list-item-title class="title font-weight-medium">BUETIAN</v-list-item-title>
            </v-list-item>
            <v-divider></v-divider>
            <v-expansion-panels flat focusable popout>
                <v-expansion-panel>
                    <v-expansion-panel-header
                        style="padding: 16px"
                        expand-icon="$vuetify.icons.caretDown"
                    >Explore</v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <v-list>
                            <v-list-item v-for="(project, index) in projects" :key="index">
                                <v-list-item-title>{{ project.name }}</v-list-item-title>
                                <v-list-item-icon>
                                    <v-icon>$vuetify.icons.externalLink</v-icon>
                                </v-list-item-icon>
                            </v-list-item>
                        </v-list>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
            <v-divider></v-divider>

            <div v-if="isLoggedIn">
                <v-list-item @click="visitProfile">
                    <a>Your profile</a>
                </v-list-item>
                <v-list-item @click="logOut">
                    <a>Log out</a>
                </v-list-item>
            </div>
            <div v-else>
                <v-list-item>
                    <router-link to="/login">Login</router-link>
                </v-list-item>
                <v-list-item>
                    <router-link to="/signup">Signup</router-link>
                </v-list-item>
            </div>
            <v-divider></v-divider>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    props: ["value"],
    data() {
        return {
            
        };
    },
    computed: {
        ...mapGetters("auth", ["isLoggedIn"]),
        drawer: {
            get() {
                return this.value;
            },
            set(val) {
                this.$emit("input", val);
            }
        }
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
    color: black;
}

.v-divider {
    margin: 8px 32px;
}
</style>