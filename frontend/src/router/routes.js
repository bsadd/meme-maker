const routes = [{
        path: '/',
        component: () =>
            import ('@/views/Home.vue'),
        meta: {
            guest: true
        }
    },
    {
        path: '/login',
        name: 'login',
        component: () =>
            import ('@/views/LoginPopup.vue'),
        meta: {
            guest: true
        }
    },
    {
        path: '/signup',
        component: () =>
            import ('@/views/Signup.vue'),
        children: [{
                path: '',
                component: () =>
                    import ('@/components/forms/SignupForm.vue'),
                meta: {
                    guest: true
                }
            },
            {
                path: 'social',
                props: { signup_method: 'social' },
                component: () =>
                    import ('@/components/forms/RegistrationForm.vue'),
                meta: {
                    requiresAuth: true
                }
            },
            {
                path: 'email',
                props: { signup_method: 'email' },
                component: () =>
                    import ('@/components/forms/RegistrationForm.vue'),
                meta: {
                    guest: true
                }
            }
        ]
    },
    {
        path: '/search',
        name: 'search',
        component: () =>
            import ('@/views/Search.vue'),
        meta: {
            guest: true
        }
    }
]

export default routes