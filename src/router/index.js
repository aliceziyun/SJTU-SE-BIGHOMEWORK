import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../view/homeView.vue";
import LoginView from "../view/loginView.vue";
import HelpPage from "../pages/helpPage.vue";
import DocPage from "../pages/docPage.vue";
import DocBinPage from "../pages/docbinPage.vue";
import DocEditor from "../pages/doc2Page.vue";
import TeamPage from "../pages/teamPage.vue";
import UserPage from "../pages/userPage.vue";

Vue.use(VueRouter);

/*
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
   return originalPush.call(this, location).catch(err => err)
}
*/

const routes = [
  {
    path: "/home",
    name: "home",
    component: HomeView,
    children: [
      {
        path: "/help",
        component: HelpPage,
        //component: () => import('../components/Help.vue')
      },
      {
        path: "/doc/:id",
        component: DocPage,
        //component: ()=> import('../components/pages/docPage.vue')
      },
      {
        path: "/bin/:id",
        component: DocBinPage,
        //component: ()=> import('../components/pages/docPage.vue')
      },
      {
        path: "/team/:id",
        component: TeamPage,
      },
      {
        path: '/message',
        name: 'noticeIndex',
        component: require('@/components/notice/noticeIndex.vue').default,
        children: [
          {
            path: '/invitation',
            component: require('@/components/notice/invitationMsg.vue').default
          },
          {
            path: '/application',
            component: require('@/components/notice/applicationMsg.vue').default
          },
          {
            path: '/notice',
            component: require('@/components/notice/noticeHandle.vue').default
          }
        ]
      },
    ],
  },
  {
    path: "/",
    name: "LoginView",
    component: LoginView,
  },
  {
    path: "/editor/:id",
    name: "DocEditor",
    component: DocEditor,
  },
  {
    path: "/personal-page/:username",
    component: UserPage,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  //to到哪儿  from从哪儿离开  next跳转 为空就是放行
  if (to.path === "/") {
    //如果跳转为登录，就放行
    next();
  } else {
    //取出localStorage判断
    let token = localStorage.getItem("token");
    if (token == null || token === "") {
      console.log("请先登录3");
      console.log(to.path);
      alert("请先登录！");
      //next({name:'loginView'});
    } else {
      next();
    }
  }
});
export default router;
