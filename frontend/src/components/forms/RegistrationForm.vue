<template>
    <v-row justify="center" align="center" style="height: 100%">
        <v-card flat class="pa-5" :width="cardWidth" style="padding: 50px !important">
            <v-row justify="center">
                <v-col cols="12">
                    <v-form ref="form" v-model="valid">
                        <v-row>
                            <v-col>
                                <div
                                    class="mb-5"
                                >Provide the following information to complete your registration</div>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col>
                                <v-subheader>E-mail</v-subheader>
                                <v-text-field
                                    v-model="email"
                                    required
                                    :disabled="email_disabled"
                                    :rules="rules.email"
                                    filled
                                    dense
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col>
                                <v-subheader>First Name</v-subheader>
                                <v-text-field
                                    filled
                                    dense
                                    v-model="first_name"
                                    :rules="rules.name"
                                    required
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-subheader>Last Name</v-subheader>
                                <v-text-field
                                    filled
                                    dense
                                    v-model="last_name"
                                    :rules="rules.name"
                                    required
                                ></v-text-field>
                            </v-col>
                        </v-row>


                        <v-row v-if="signup_method == 'email'">
                            <v-col>
                                <v-subheader>Password</v-subheader>
                                <v-text-field
                                    filled
                                    dense
                                    v-model="password"
                                    :rules="rules.name"
                                    required
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row v-if="signup_method == 'email'">
                            <v-col>
                                <v-subheader>Confirm Password</v-subheader>
                                <v-text-field
                                    filled
                                    dense
                                    v-model="confirm_password"
                                    :rules="rules.password"
                                    required
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col>
                                <v-checkbox
                                    v-model="checkbox"
                                    :rules="[(v) => !!v || 'You must agree to continue!']"
                                    required
                                >
                                    <template v-slot:label>
                                        <span>
                                            I accept the
                                            <a
                                                href="#"
                                                class="pl-1"
                                            >Terms and Conditions</a>
                                        </span>
                                    </template>
                                </v-checkbox>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col>
                                <v-btn
                                    :disabled="!valid"
                                    color="primary"
                                    block
                                    @click="completeRegistration"
                                    class="loading-btn"
                                >
                                    REGISTER
                                    <v-progress-linear
                                        :active="registering"
                                        absolute
                                        bottom
                                        color="accent"
                                        indeterminate
                                    ></v-progress-linear>
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-col>
            </v-row>
        </v-card>
    </v-row>
</template>

<script>
export default {
    props: ["signup_method"],
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
        },
        email_disabled() {
            if (
                this.signup_method == "social" ||
                this.signup_method == "referral"
            ) {
                return true;
            } else {
                return false;
            }
        },
        sid_disabled() {
            if (this.signup_method == "referral") {
                return true;
            } else {
                return false;
            }
        }
    },
    data() {
        return {
            email: null,
            first_name: null,
            last_name: null,
            password: null,
            confirm_password: null,
            valid: false,
            registering: false,
            registration_complete: false,
            rules: {
                name: [v => !!v || "This field is required"],
                email: [
                    v => !!v || "This field is required",
                    v => /.+@.+\..+/.test(v) || "E-mail must be valid"
                ],
                password: [
                    v => !!v || "This field is required",
                    v => this.password == v || "Passwords don't match"
                ]
            },
            checkbox: false
        };
    },
    created() {
        if (this.signup_method == "social") {
            this.email = this.$store.state.profile.email;
            this.first_name = this.$store.state.profile.first_name;
            this.last_name = this.$store.state.profile.last_name;
        }
    },
    methods: {
        async completeRegistration() {
            if (this.$refs.form.validate()) {
                this.registering = true;

                if (this.signup_method == "social") {
                    const data = {
                        first_name: this.first_name,
                        last_name: this.last_name,
                        student_id: this.student_id
                    };
                    try {
                        await this.$store.dispatch(
                            "profile/updateCurrentUserProfile",
                            data
                        );
                        this.registration_complete = true;
                        setTimeout(() => this.$router.push("/"), 1000);
                    } catch (error) {
                        // TODO: handle error
                        this.$router.push("/");
                    }
                }
            }
        }
    }
};
</script>

<style scoped>
.v-card {
    border-radius: 0px !important;
}

.col {
    padding-top: 0px;
    padding-bottom: 0px;
}

a {
    text-decoration: none;
}
</style>
