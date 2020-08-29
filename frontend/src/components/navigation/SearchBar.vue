<template>
    <v-combobox
        :items="items"
        :search-input.sync="search"
        :loading="is_loading"
        :menu-props="{ closeOnClick: true, closeOnContentClick: true }"
        loader-height="10"
        solo
        dense
        clearable
        clear-icon="$close"
        prepend-inner-icon="$search"
        append-icon
        rounded
        placeholder="Search"
        hide-details
        hide-selected
        hide-no-data
        item-text="name"
        item-value="symbol"
        @keyup.enter="redirectToSearch"
    ></v-combobox>
</template>

<script>
export default {
    data: () => ({
        is_loading: false,
        items: [],
        search: null
    }),
    methods: {
        redirectToSearch() {
            this.$router.push("/search");
        }
    },
    watch: {
        search(val) {
            console.log(val);
            // Items have already been loaded
            if (this.items.length > 0) return;

            this.is_loading = true;

            // Lazily load input items
            fetch("https://api.coingecko.com/api/v3/coins/list")
                .then(res => res.clone().json())
                .then(res => {
                    this.items = res;
                })
                .catch(err => {
                    console.log(err);
                })
                .finally(() => (this.is_loading = false));
        }
    }
};
</script>

<style scoped>
</style>