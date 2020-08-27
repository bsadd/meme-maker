<template>
    <v-card
    class="my-3 py-2"
    width="100%"
    color="secondary"
    >
        <v-card-title class="py-0">
            <router-link :to="'/post/' + id" id="title-link">
                {{ username }}
            </router-link>
        </v-card-title>
        <v-card-text class="py-0">{{ caption }}</v-card-text>
        <img 
        v-bind:src="image"
        height="400"
        contain
        />
    </v-card>
</template>

<script>
export default {
    props: [
        'id',
        'username',
        'caption',
        'image'
    ],
    computed: {
        
    }
}
</script>

<style scoped>

a {
    padding: 0px;
    color: black;
}

#title-link {
    color: darkred;
}

#title-link:hover {
    text-decoration: underline;
}
</style>