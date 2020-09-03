<template>
    <div>
        <card-loading v-if="loading"></card-loading>
        <v-list v-else>
            <v-list-item
            v-for="(post, index) in search_results"
            :key="index"
            >
                <profile-card
                :id="post.id"
                :username="post.user.username"
                :caption="post.caption"
                :image="post.image"
                ></profile-card>
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
            'search_results'
        ])
    },
    components: {
        'card-loading': () => import('@/components/loading/CardLoading'),
        'profile-card': () => import('@/components/common/ProfileCard')
    },
    created () {
        this.$store.dispatch('newsfeed/searchRequest');
    }
}
</script>

<style>

</style>