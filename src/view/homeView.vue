<template>
  <a-layout id="components-layout-demo-fixed-sider">
    <a-layout-sider
      :style="{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0 }"
    >
      <div style="background: rgb(29, 130, 72)" class="logo">
        <img src="../assets/cabbage.png" height="40px" />
        Cabbage
      </div>
      <a-menu
        style="background: rgb(29, 130, 72); color: white"
        mode="inline"
        @select="menuClick"
      >
        <a-menu-item key="user">
          <a-icon type="user" />
          <span>PERSONAL PAGE</span>
        </a-menu-item>
        <a-menu-item key="doc">
          <a-icon type="file" />
          <span>MY DOCS</span>
        </a-menu-item>
        <a-menu-item key="bin">
          <a-icon type="delete" />
          <span>BIN</span>
        </a-menu-item>
        <a-menu-item key="team">
          <a-icon type="team" />
          <span>MY TEAM</span>
        </a-menu-item>
        <a-menu-item key="help">
          <a-icon type="question" />
          <span>HELP</span>
        </a-menu-item>
        <a-sub-menu key="sub">
          <template #title>MESSAGE</template>
          <a-menu-item key="application">
            <a-icon type="video-camera" />
            <span class="nav-text">application</span>
          </a-menu-item>
          <a-menu-item key="invitation">
            <a-icon type="upload" />
            <span class="nav-text">invitation</span>
          </a-menu-item>
          <a-menu-item key="notice">
            <a-icon type="info-circle" />
            <span class="nav-text">notice</span>
          </a-menu-item>
        </a-sub-menu>
      </a-menu>
    </a-layout-sider>
    <a-layout :style="{ marginLeft: '200px' }">
      <!-- <a-layout-header :style="{ background: '#fff', padding: 0 }" /> -->
      <a-layout-content :style="{ margin: '10px 8px 0', overflow: 'initial' }">
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
        this is Cabbage Doc~ @sjtu
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
          this.$router.push("/doc/" + localStorage.getItem("userid"));
          break;
        case "bin":
          this.$router.push("/bin/" + localStorage.getItem("userid"));
          break;
        case "team":
          this.$router.push("/team/" + localStorage.getItem("userid"));
          break;
        case "user":
          this.$router.push("/personal-page/" + localStorage.getItem("token"));
          break;
        case "message":
          this.$router.push("/message/");
          break;
        // case "nav-text":
        //   this.$router.push("")
        case "application":
          this.$router.push("/application");
          break;
        case "invitation":
          this.$router.push("/invitation");
          break;
        case "notice":
          this.$router.push("/notice/");
          break;
      }
    },
  },
};
</script>

<style scoped>
#components-layout-demo-fixed-sider .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  font-size: 20px;
  color: white;
  margin: 16px;
}
</style>
