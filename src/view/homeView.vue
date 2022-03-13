<template>
  <a-layout id="components-layout-demo-fixed-sider">
    <a-layout-sider
      :style="{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0 }"
    >
      <div style="background:black" class="logo">
        <img src="../assets/cabbage.png" height=40px/>
        Cabbage
      </div>
      <a-menu
        theme="dark"
        mode="inline"
        :default-selected-keys="['doc']"
        @select="menuClick"
      >
        <a-menu-item key="user">
          <a-icon type="user" />
          <span>个人主页</span>
        </a-menu-item>
        <a-menu-item key="doc">
          <a-icon type="file" />
          <span>我的文档</span>
        </a-menu-item>
        <a-menu-item key="bin">
          <a-icon type="delete" />
          <span>回收站</span>
        </a-menu-item>
        <a-menu-item key="team">
          <a-icon type="team" />
          <span>团队</span>
        </a-menu-item>
        <a-menu-item key="help">
          <a-icon type="question" />
          <span>帮助</span>
        </a-menu-item>
        <a-menu-item key="message">
          <a-icon type="bell" />
          <span>消息</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout :style="{ marginLeft: '200px' }">
      <!-- <a-layout-header :style="{ background: '#fff', padding: 0 }" /> -->
      <a-layout-content :style="{ margin: '10px 8px 0', overflow: 'initial'}">
        <div
          :style="{
            padding: '24px',
            background: '#fff',
            textAlign: 'center',
            height: '738px',
          }"
        >
          <router-view></router-view>
        </div>
      </a-layout-content>
      <a-layout-footer :style="{ textAlign: 'center' }">
        恭喜你发现了卷心菜文档
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
 
<script>
export default {
  name: "HomeView",
  data() {
    return {};
  },
  methods: {
    menuClick(key) {
      console.log(key);
      switch (key.key) {
        case "help":
          this.$router.push("/help");
          break;
        case "doc":
          this.$router.push("/doc");
          break;
        case "team":
          this.$router.push("/team");
          break;
        case "user":
          this.$router.push("/personal-page");
          break;
      }
    },
  },
};
</script>


<style>
#components-layout-demo-fixed-sider .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  font-size: 20px;
  color: white;
  margin: 16px;
}
</style>
