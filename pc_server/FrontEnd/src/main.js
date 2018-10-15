import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'

import router from './router'
import "./assets/fonts/google_icon/google_icon.css"
import "./assets/fonts/roboto/Roboto.css"

Vue.config.productionTip = false

new Vue({
        router,
        render: h => h(App)
    }).$mount('#app')
    // new Vue({
    //     el: '#app',
    //     router,
    //     components: { App },
    //     template: '<App/>'
    // })