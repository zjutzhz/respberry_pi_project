import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ControlPanel from '@/components/ControlPanel'
import Main from '@/components/Main2'
import DashBoard from '@/modules/dashboard/Main'

Vue.use(Router)

export default new Router({
    routes: [{
        path: '/',
        name: 'HelloWorld',
        props: true,
        component: HelloWorld
    }, {
        path: "/control_panel/:port",
        name: "ControlPanel",
        props: true,
        component: ControlPanel
    }, {
        path: "/main",
        component: Main
    }, {
        path: "/dashboard",
        component: DashBoard
    }]
})