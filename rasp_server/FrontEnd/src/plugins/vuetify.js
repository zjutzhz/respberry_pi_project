import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import zhHans from 'vuetify/es5/locale/zh-Hans'

Vue.use(Vuetify, {
  iconfont: 'md',
  lang: {
    locales: { zhHans },
    current: 'zh-Hans'
  },
})
