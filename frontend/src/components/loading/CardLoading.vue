<template>
    <div>
    <content-loader
    height="50"
    class="pa-5"
    v-for="i in [1, 2, 3, 4, 5]"
    :key="i"
    >
        <rect x="0" y="0" rx="3" ry="3" width="60%" height="10" />
        <rect x="0" y="15" rx="3" ry="3" width="80%" height="15" />
        <rect x="0" y="35" rx="3" ry="3" width="90%" height="5" />
        <rect x="0" y="45" rx="3" ry="3" width="90%" height="5" />
    </content-loader></div>
</template>

<script>
import { ContentLoader } from 'vue-content-loader';

export default {
    components: {
        'content-loader': ContentLoader
    }
}
</script>