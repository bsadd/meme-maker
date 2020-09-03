<template>
    <v-card width="25%" flat>
        <v-list shaped>
            <v-list-item-group>
                <v-list-item v-if="isLoggedIn" @click="visitProfile">
                    <v-list-item-avatar size="20" class="mr-3" color="primary">{{ getInitials }}</v-list-item-avatar>

                    <v-list-item-title>
                        <a href="#">{{ getFullName }}</a>
                    </v-list-item-title>
                </v-list-item>

                <v-list-item v-if="isLoggedIn">
                    <v-list-item-icon class="mr-0">
                        <v-icon size="20" class="mr-3" color="primary">$vuetify.icons.referUser</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>
                        <a href="#">Refer Someone</a>
                    </v-list-item-title>
                </v-list-item>

                <v-divider class="mb-2" v-if="isLoggedIn"></v-divider>
                
            </v-list-item-group>
        </v-list>
    </v-card>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    data() {
        return {
            internal_links: [
                {
                    title: "About Us",
                    url: "#",
                    icon: "about"
                },
                {
                    title: "Workplace Feedback",
                    url: "#",
                    icon: "feedback"
                }
            ],
            external_links: [
                {
                    title: "Meme Maker",
                    url: "#",
                    icon: "memeMaker"
                },
                {
                    title: "Buetian Blog",
                    url: "#",
                    icon: "blog"
                }
            ]
        };
    },
    computed: {
        ...mapGetters("auth", ["isLoggedIn"]),
        ...mapGetters("profile", ["getInitials", "getFullName"])
    },
    methods: {
        visitProfile() {
            const uuid = this.$store.state.profile.uuid;
            this.$router.push({ name: "profile", params: { uuid } });
        }
    }
};
</script>

<style scoped>
a {
    padding: 0px;
    color: black;
}

.v-list-item {
    margin-bottom: 8px !important;
}

.v-card {
    border-radius: 0px !important;
    position: fixed !important;
    height: 100%;
}
</style>