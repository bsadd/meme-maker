<template>
    <v-row justify="center" align="center" style="height: 100%">
        <v-card flat style="padding: 50px" :width="cardWidth">
            <v-card-title class="pt-0">
                <span>
                    <big>Log in to your account</big>
                </span>
            </v-card-title>

            <v-card-text>
                <v-row>
                    <v-col cols="12">
                        <facebook-login @socialClick="socialLogin"></facebook-login>
                    </v-col>
                    <v-col cols="12">
                        <google-login @socialClick="socialLogin"></google-login>
                    </v-col>

                    <v-col cols="12">
                        <v-divider id="or-divider"></v-divider>
                    </v-col>

                    <v-col cols="12">
                        <v-form ref="form" v-model="valid">
                            <v-col cols="12" class="py-0">
                                <v-subheader>E-mail</v-subheader>
                                <v-text-field
                                    v-model="email"
                                    required
                                    :rules="rules.email"
                                    filled
                                    dense
                                ></v-text-field>
                            </v-col>

                            <v-col cols="12" class="py-0">
                                <v-subheader>Password</v-subheader>
                                <v-text-field
                                    filled
                                    dense
                                    v-model="password"
                                    :rules="rules.name"
                                    required
                                ></v-text-field>
                            </v-col>

                            <v-col cols="12">
                                <v-btn
                                    block
                                    color="primary"
                                    class="loading-btn"
                                    @click="emailLogin"
                                >
                                    LOG IN
                                    <v-progress-linear
                                        :active="loggingIn"
                                        absolute
                                        bottom
                                        color="accent"
                                        indeterminate
                                    ></v-progress-linear>
                                </v-btn>
                            </v-col>
                        </v-form>
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
            email: null,
            password: null,
            valid: false,
            loggingIn: false,
            rules: {
                name: [v => !!v || "This field is required"],
                email: [
                    v => !!v || "This field is required",
                    v => /.+@.+\..+/.test(v) || "E-mail must be valid"
                ]
            }
        };
    },
    components: {
        FacebookLogin,
        GoogleLogin
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
    methods: {
        async socialLogin(settings) {
            const params = {
                grant_type: "convert_token",
                client_id: process.env.VUE_APP_CLIENT_ID,
                client_secret: process.env.VUE_APP_CLIENT_SECRET,
                backend: settings.backend,
                token: settings.token
            };

            await this.$store.dispatch("auth/exchangeSocialToken", params);
            await this.$store.dispatch("profile/fetchCurrentUserProfile");

            this.$router.push("/");
        },
        async emailLogin() {
            if (this.$refs.form.validate()) {
                this.loggingIn = true;
                const params = {
                    grant_type: "password",
                    client_id: process.env.VUE_APP_CLIENT_ID,
                    client_secret: process.env.VUE_APP_CLIENT_SECRET,
                    username: this.email,
                    password: this.password
                };

                try {
                    await this.$store.dispatch(
                        "auth/loginWithCredentials",
                        params
                    );
                    await this.$store.dispatch(
                        "profile/fetchCurrentUserProfile"
                    );
                    this.$router.push("/");
                } catch (error) {
                    this.loggingIn = false;
                }
            }
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

#login-btn >>> .v-btn__content {
    height: 100%;
}
</style>