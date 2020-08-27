import { library } from '@fortawesome/fontawesome-svg-core' // Core SVG
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome' // Integration
import Vue from 'vue'

Vue.component('font-awesome-icon', FontAwesomeIcon)

import {
    faFacebookF,
    faGoogle,
    faLinkedinIn
} from '@fortawesome/free-brands-svg-icons'
import {
    faGraduationCap,
    faMapMarkerAlt,
    faUniversity,
    faBriefcase,
    faUserCircle,
    faSignOutAlt,
    faUsers,
    faPhone,
    faLink,
    faSearch,
    faCaretDown,
    faBars,
    faTimes,
    faChevronLeft,
    faChevronRight,
    faAngleRight,
    faCheckSquare,
    faCheck,
    faDotCircle,
    faPen,
    faPlus,
    faExternalLinkAlt,
    faBlog,
    faInfoCircle,
    faUserPlus,
    faArrowUp,
    faExclamationCircle,
    faIdCard,
    faTint,
    faHotel
} from '@fortawesome/free-solid-svg-icons'
import {
    faEnvelope,
    faTimesCircle,
    faSquare,
    faCircle,
    faCommentAlt,
    faLaughSquint
} from '@fortawesome/free-regular-svg-icons'

library.add(
    faFacebookF,
    faGoogle,
    faLinkedinIn,
    faGraduationCap,
    faMapMarkerAlt,
    faUniversity,
    faBriefcase,
    faUserCircle,
    faSignOutAlt,
    faUsers,
    faPhone,
    faEnvelope,
    faLink,
    faSearch,
    faCaretDown,
    faTimes,
    faTimesCircle,
    faBars,
    faChevronLeft,
    faChevronRight,
    faAngleRight,
    faSquare,
    faCheckSquare,
    faCheck,
    faCircle,
    faDotCircle,
    faCommentAlt,
    faExternalLinkAlt,
    faPen,
    faPlus,
    faLaughSquint,
    faBlog,
    faInfoCircle,
    faUserPlus,
    faArrowUp,
    faExclamationCircle,
    faIdCard,
    faTint,
    faHotel
)

const CUSTOM_ICONS = {
    facebook: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fab', 'facebook-f']
        }
    },
    google: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fab', 'google']
        }
    },
    linkedin: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fab', 'linkedin-in']
        }
    },
    graduation: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'graduation-cap']
        }
    },
    location: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'map-marker-alt']
        }
    },
    university: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'university']
        }
    },
    work: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'briefcase']
        }
    },
    profile: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'user-circle']
        }
    },
    logout: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'sign-out-alt']
        }
    },
    users: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'users']
        }
    },
    feedback: {
        component: FontAwesomeIcon,
        props: {
            icon: ['far', 'comment-alt']
        }
    },
    phone: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'phone']
        }
    },
    email: {
        component: FontAwesomeIcon,
        props: {
            icon: ['far', 'envelope']
        }
    },
    link: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'link']
        }
    },
    search: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'search']
        }
    },
    caretDown: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'caret-down']
        }
    },
    timesCircle: {
        component: FontAwesomeIcon,
        props: {
            icon: ['far', 'times-circle']
        }
    },
    hamburger: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'bars']
        }
    },
    close: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'times']
        }
    },
    edit: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'pen']
        }
    },
    add: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'plus']
        }
    },
    radioOn: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'dot-circle']
        }
    },
    externalLink: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'external-link-alt']
        }
    },
    right: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'angle-right']
        }
    },
    memeMaker: {
        component: FontAwesomeIcon,
        props: {
            icon: ['far', 'laugh-squint']
        }
    },
    blog: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'blog']
        }
    },
    about: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'info-circle']
        }
    },
    referUser: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'user-plus']
        }
    },
    arrowUp: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'arrow-up']
        }
    },
    error: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'exclamation-circle']
        }
    },
    id: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'id-card']
        }
    },
    hall: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'hotel']
        }
    },
    blood: {
        component: FontAwesomeIcon,
        props: {
            icon: ['fas', 'tint']
        }
    }
}

export { CUSTOM_ICONS }