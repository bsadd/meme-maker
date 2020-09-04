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
        <v-card-text class="py-0" >{{(nlike?nlike:0)+(nlove?nlove:0)+
            (nhaha?nhaha:0)+(nwow?nwow:0)+(nsad?nsad:0)+(nangry?nangry:0)}} people reacted this post</v-card-text>
        <v-row>
            <v-col>
                <v-btn
                block
                color="primary"
                class="btn"
                @click="reactOnPost"
                >React</v-btn>
            </v-col>
            <v-col>
                <v-btn
                block
                color="primary"
                class="btn"
                @click="reactOnPost"
                >Comment</v-btn>
            </v-col>
            <v-col>
                <v-btn
                block
                color="primary"
                class="btn"
                @click="reactOnPost"
                >Create</v-btn>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
export default {
    props: [
        'id',
        'username',
        'caption',
        'image',
        'nlike',
        'nlove',
        'nhaha',
        'nwow',
        'nsad',
        'nangry'
    ],
    computed: {
        
    },
    methods: {
        reactOnPost(){
            console.log("reaction");
        }
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