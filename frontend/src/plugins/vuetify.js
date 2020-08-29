import { CUSTOM_ICONS } from "./fontAwesome"
import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
    icons: {
        iconfont: 'faSvg',
        values: CUSTOM_ICONS
    },
    theme: {
        options: {
            customProperties: true
        },
        themes: {
            light: {
                primary: '#8b0000',
                secondary: '#fdfafa',
                accent: colors.orange.lighten5,
                error: colors.red,
                info: colors.red.lighten5,
                success: colors.red.lighten4,
                warning: colors.red.darken4,
            },
            dark: {
                primary: colors.blue.lighten3,
            },
        },
    },
});