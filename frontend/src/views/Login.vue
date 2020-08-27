<template>
    <v-row style="height: 100%">
        <v-col cols="12" md="7" style="height: 100%;">
            <login-form></login-form>
        </v-col>
    </v-row>
</template> 


<script>
import LoginForm from "@/components/forms/LoginForm";

export default {
    components: {
        LoginForm
    },
    methods: {}
};
</script>

<style scoped>
#welcome-card {
    border-radius: 0px !important;
    padding: 50px;
}
</style>