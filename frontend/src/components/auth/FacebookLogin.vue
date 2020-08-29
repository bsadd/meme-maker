<template>
    <div>
        <v-facebook-login-scope :app-id="app_id">
            <v-btn
                class="white--text"
                large
                rounded
                color="#3b5999"
                style="width: 100%;"
                slot-scope="scope"
                @click="login(scope)"
            >
                <v-row align="center" justify="start">
                    <v-col cols="2" class="pa-0">
                        <v-icon class="mr-2">$vuetify.icons.facebook</v-icon>
                    </v-col>
                    <v-col cols="8" class="pa-0">
                        <span v-if="!signup" style="align-self: center">Log in with Facebook</span>
                        <span v-else style="align-self: center">Sign up with Facebook</span>
                    </v-col>
                </v-row>
            </v-btn>
        </v-facebook-login-scope>
    </div>
</template>

<script>
import { VFBLoginScope as VFacebookLoginScope } from "vue-facebook-login-component";

export default {
    props: {
        signup: {
            type: Boolean,
            default: false
        }
    },
    components: {
        VFacebookLoginScope
    },
    data() {
        return {
            app_id: process.env.VUE_APP_SOCIAL_AUTH_FACEBOOK_KEY
        };
    },
    methods: {
        async login(scope) {
            const response = await scope.login();

            const settings = {
                backend: "facebook",
                token: response.authResponse.accessToken
            };

            this.$emit("socialClick", settings);
        }
    }
};
</script>

<style>
</style>