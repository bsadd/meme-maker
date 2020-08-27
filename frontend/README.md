# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# Setup
For social login and api requests to work, you'll need an `.env` file in the root directory containing the following environment variables :

- VUE_APP_BASE_URL
    - url of the locally running django server
    - value : `http://localhost:8000` 
    - all api requests are made to this url

- VUE_APP_SOCIAL_AUTH_FACEBOOK_KEY
    - id of the facebook app that is connected to our project
    - value : `552300925459826`

- VUE_APP_GOOGLE_OAUTH_CLIENT_ID
    - id of the google app that is connected to our project
    - value : `41946015345-4dnp3gug0vel2app9arekvvj3g5rogqs.apps.googleusercontent.com`

- VUE_APP_CLIENT_ID, VUE_APP_CLIENT_SECRET
    - you will need access to client id and client secret to be able to make api requests
    - read [this](https://github.com/RealmTeam/django-rest-framework-social-oauth2#setting-up-a-new-application) to get these two values

# Naming Conventions

## variables
- snake_case 

## functions
- camelCase

## components
- PascalCase 
- preferably two or more words

## views
- PascalCase
- preferably one word

## vuex store
- state : snake_case
- getters : camelCase
- mutations : snake_case, all caps
- actions : camelCase

## css selectors
- kebab-case