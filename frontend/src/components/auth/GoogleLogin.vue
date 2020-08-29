<template>
    <div style="width: 100%;">
        <GoogleLogin
            :params="params"
            :onSuccess="onSuccess"
            :onFailure="onFailure"
            style="width: 100%;"
        >
            <v-btn class="white--text" large rounded color="#4284f4" style="width: 100%;">
                <v-row align="center" justify="start">
                    <v-col cols="2" class="pa-0">
                        <v-icon class="mr-2">$vuetify.icons.google</v-icon>
                    </v-col>
                    <v-col cols="8" class="pa-0">
                        <span v-if="!signup" style="align-self: center">Log in with Google</span>
                        <span v-else style="align-self: center">Sign up with Google</span>
                    </v-col>
                </v-row>
            </v-btn>
        </GoogleLogin>
    </div>
</template>

<script>
import { GoogleLogin } from "vue-google-login";

export default {
    props: {
        signup: {
            type: Boolean,
            default: false
        }
    },
    components: {
        GoogleLogin
    },
    data() {
        return {
            params: {
                client_id: process.env.VUE_APP_GOOGLE_OAUTH_CLIENT_ID
            }
        };
    },
    methods: {
        onSuccess(user) {
            const accessToken = user.wc.access_token;

            const settings = {
                backend: "google-oauth2",
                token: accessToken
            };

            this.$emit("socialClick", settings);
        },
        onFailure(errorData) {
            // The errorData variable contains failure details
            console.log(errorData);
        }
    }
};
</script>

<style>
</style>