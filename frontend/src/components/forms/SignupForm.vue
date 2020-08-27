<template>
    <v-row justify="center" align="center" style="height: 100%">
        <v-card flat v-if="authorizing" style="border-radius: 0px !important">
            <v-card-title>Authorizing</v-card-title>
            <v-progress-linear indeterminate height="5px"></v-progress-linear>
        </v-card>

        <v-card flat v-else style="padding: 50px" :width="cardWidth">
            <v-card-title class="pt-0">
                <span>
                    <big>Create Your Account</big>
                </span>
            </v-card-title>
            <v-card-text>
                <v-row>
                    <v-col cols="12">
                        <facebook-login :signup="signup" @socialClick="socialSignup"></facebook-login>
                    </v-col>
                    <v-col cols="12">
                        <google-login :signup="signup" @socialClick="socialSignup"></google-login>
                    </v-col>

                    <v-col cols="12">
                        <v-divider id="or-divider"></v-divider>
                    </v-col>

                    <v-col cols="12">
                        <v-btn
                            class="white--text"
                            large
                            rounded
                            color="primary"
                            style="width: 100%;"
                            @click="emailSignup"
                        >
                            <v-row align="center" justify="start">
                                <v-col cols="2" class="pa-0">
                                    <v-icon class="mr-2">$vuetify.icons.email</v-icon>
                                </v-col>
                                <v-col cols="8" class="pa-0">
                                    <span style="align-self: center">Sign up with Email</span>
                                </v-col>
                            </v-row>
                        </v-btn>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-row>
</template> 

<script>
import FacebookLogin from "@/components/auth/FacebookLogin";
import GoogleLogin from "@/components/auth/GoogleLogin";

export default {
    data() {
        return {
            authorizing: false,
            signup: true
        };
    },
    computed: {
        cardWidth() {
            switch (this.$vuetify.breakpoint.name) {
                case "xs":
                    return "100%";
                case "sm":
                    return "70%";
                case "md":
                    return "70%";
                case "lg":
                    return "70%";
                case "xl":
                    return "70%";
                default:
                    return "100%";
            }
        }
    },
    components: {
        FacebookLogin,
        GoogleLogin
    },
    methods: {
        emailSignup() {
            this.$router.push("/signup/email");
        },
        async socialSignup(settings) {
            const params = {
                grant_type: "convert_token",
                client_id: process.env.VUE_APP_CLIENT_ID,
                client_secret: process.env.VUE_APP_CLIENT_SECRET,
                backend: settings.backend,
                token: settings.token
            };

            this.authorizing = true;
            await this.$store.dispatch("auth/exchangeSocialToken", params);
            await this.$store.dispatch("profile/fetchCurrentUserProfile");

            this.$router.replace("/signup/social");
        }
    }
};
</script>

<style scoped>
#or-divider {
    text-align: center;
    margin: 20px 0px;
}

#or-divider::after {
    content: "OR";
    display: inline-block;
    position: relative;
    top: -10px;
    padding: 0 16px;
    background: #fff;
}
</style>