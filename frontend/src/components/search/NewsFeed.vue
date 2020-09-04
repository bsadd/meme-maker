<template>
    <div>
        <card-loading v-if="loading"></card-loading>
        <v-list v-else>
            <v-list-item
            v-for="(post, index) in post_list"
            :key="index"
            >
                <meme-card
                :id="post.id"
                :username="post.user.username"
                :caption="post.caption"
                :image="post.image"
                :nlike="post.reaction_counts.Like"
                :nlove="post.reaction_counts.Love"
                :nhaha="post.reaction_counts.Haha"
                :nwow="post.reaction_counts.Wow"
                :nsad="post.reaction_counts.Sad"
                :nangry="post.reaction_counts.Angry"
                ></meme-card>
            </v-list-item>
        </v-list>
    </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
    computed: {
        ...mapState('newsfeed', [
            'loading',
            'post_list'
        ])
    },
    
    components: {
        'card-loading': () => import('@/components/loading/CardLoading'),
        'meme-card': () => import('@/components/common/MemeCard'),
    },
    created () {
        this.$store.dispatch('newsfeed/searchRequest');
    }
}
</script>

<style>

</style>