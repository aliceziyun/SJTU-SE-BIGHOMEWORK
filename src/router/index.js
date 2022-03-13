import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../view/homeView.vue'
import LoginView from '../view/loginView.vue'
import HelpPage from '../components/pages/helpPage.vue'
import DocPage from '../components/pages/docPage.vue'
import TeamPage from '../components/pages/teamPage.vue'
import UserPage from '../components/pages/userPage.vue'

Vue.use(VueRouter)

/*
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
   return originalPush.call(this, location).catch(err => err)
}
*/

export default new VueRouter({
    routes: [
        {
            path: '/home',
            name: 'home',
            component: HomeView,
            children: [
                {
                    path: '/help',
                    component: HelpPage
                    //component: () => import('../components/Help.vue')
                },
                {
                    path: '/doc',
                    component: DocPage
                    //component: ()=> import('../components/pages/docPage.vue')
                },
                {
                    path: '/team',
                    component: TeamPage
                },
                {
                    path: "/personal-page",
                    component: UserPage,
                },
            ]
        },
        {
            path: "/",
            name: 'LoginView',
            component: LoginView,
        },

    ]
})