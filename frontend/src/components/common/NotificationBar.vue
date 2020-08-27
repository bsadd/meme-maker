<template>
    <v-banner app color="secondary" elevation="20" :value="show">
        <template v-slot:icon>
            <v-icon medium color="primary">$vuetify.icons.error</v-icon>
        </template>
        <span class="subtitle-1 font-weight-bold" style="color: var(--v-primary-base)">{{ message }}</span>
    </v-banner>
</template>

<script>
import { mapState } from "vuex";

export default {
    computed: {
        ...mapState("error", ["show", "message"])
    }
};
</script>
