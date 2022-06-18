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

const routes = [
  {
    path: "/home",
    name: "home",
    component: HomeView,
    children: [
      {
        path: "/help",
        component: HelpPage,
      },
      {
        path: "/doc/:id",
        component: DocPage,
      },
      {
        path: "/bin/:id",
        component: DocBinPage,
      },
      {
        path: "/team/:id",
        component: TeamPage,
      },
      {
        path: "/invitation",
        component: require("@/components/notice/inviteMessage.vue").default,
      },
      {
        path: "/application",
        component: require("@/components/notice/myMessage.vue").default,
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
export default router;
