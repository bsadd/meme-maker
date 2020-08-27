<template>
  <v-card
    flat
    >
      <v-toolbar
        color="white"
        flat
      >
        <v-toolbar-title 
            style="width: 100%;"
        >
            <v-autocomplete 
                v-model="model" 
                :items="items"  
                :search-input.sync="search" 
                clearable
                clear-icon=$vuetify.icons.timesCircle
                rounded 
                hide-details 
                hide-selected 
                hide-no-data 
                item-text="name" 
                item-value="symbol" 
                outlined
                prepend-inner-icon=$vuetify.icons.search
                append-icon=""
                >
                
                <template v-slot:item="{ item }">
                    <v-list-item-content>
                        <v-list-item-title v-text="item.name"></v-list-item-title>
                    </v-list-item-content>
                </template>
            </v-autocomplete>
        </v-toolbar-title>
  
        <template v-slot:extension>
          <v-tabs
            v-model="tabs"
            align-with-title
            show-arrows
          >
            <v-tab>
                <v-icon left small>$vuetify.icons.search</v-icon>
                All
            </v-tab>
            <v-tab v-if="showFilters">
                <v-icon left small>$vuetify.icons.university</v-icon>
                Universities
            </v-tab>
            <v-tab v-if="showFilters">
                <v-icon left small>$vuetify.icons.work</v-icon>
                Companies
            </v-tab>
            <v-tab v-if="showFilters">
                <v-icon left small>$vuetify.icons.location</v-icon>
                Places
            </v-tab>
            <v-tab v-if="showFilters">
                <v-icon left small>$vuetify.icons.users</v-icon>
                People
            </v-tab>
          </v-tabs>

          <v-chip
            :input-value="showFilters"
            @click="manageFilters"
            outlined
            label
            >
            Filter
          </v-chip>
        </template>
      </v-toolbar>
  
      <v-tabs-items 
        v-model="tabs"
        >
        <v-tab-item>
          <v-card flat>
            <v-card-text>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <v-card-title class="headline">An awesome title</v-card-title>
            <v-card-text>
              <p>
                Duis lobortis massa imperdiet quam. Donec vitae orci sed dolor rutrum auctor. Vestibulum facilisis, purus nec pulvinar iaculis, ligula mi congue nunc, vitae euismod ligula urna in dolor. Praesent congue erat at massa.
              </p>
  
              <p>
                Aenean posuere, tortor sed cursus feugiat, nunc augue blandit nunc, eu sollicitudin urna dolor sagittis lacus. Pellentesque egestas, neque sit amet convallis pulvinar, justo nulla eleifend augue, ac auctor orci leo non est. Etiam sit amet orci eget eros faucibus tincidunt. Donec sodales sagittis magna.
              </p>
  
              <p class="mb-0">
                Ut leo. Suspendisse potenti. Duis vel nibh at velit scelerisque suscipit. Fusce pharetra convallis urna.
              </p>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <v-card flat>
            <v-card-title class="headline">An even better title</v-card-title>
            <v-card-text>
              <p>
                Maecenas ullamcorper, dui et placerat feugiat, eros pede varius nisi, condimentum viverra felis nunc et lorem. Sed hendrerit. Maecenas malesuada. Vestibulum ullamcorper mauris at ligula. Proin faucibus arcu quis ante.
              </p>
  
              <p class="mb-0">
                Etiam vitae tortor. Curabitur ullamcorper ultricies nisi. Sed magna purus, fermentum eu, tincidunt eu, varius ut, felis. Aliquam lobortis. Suspendisse potenti.
              </p>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    data: () => ({
        isLoading: false,
        showFilters: false,
        items: [],
        model: null,
        search: null,
        tab: null,
        tabs: null,
        text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        
    }),
    computed: {
        ...mapGetters([
            'getLoginStatus'
        ])
    },
    methods: {
        manageFilters() {
            this.showFilters = !this.showFilters;
            if (!this.showFilters) {
                this.tabs = 0;
            }
        }
    },
    watch: {
        model(val) {
            if (val != null) this.tabs = 0
            else this.tabs = null
        },
        search(val) {
            console.log(val);
            // Items have already been loaded
            if (this.items.length > 0) return

            this.isLoading = true

            // Lazily load input items
            fetch('https://api.coingecko.com/api/v3/coins/list')
                .then(res => res.clone().json())
                .then(res => {
                    this.items = res
                })
                .catch(err => {
                    console.log(err)
                })
                .finally(() => (this.isLoading = false))
        },
    },

}

</script>

<style scoped>
.v-toolbar {
    border-bottom: 1px solid lightgrey !important;
}

.v-tab {
    text-transform: none;
}
</style>