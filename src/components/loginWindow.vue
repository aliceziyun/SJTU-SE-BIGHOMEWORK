<template>
  <a-layout style="min-height:100%">
    <a-layout-content id="card">
      <a-card style="width:400px;height:500px;border-radius: 10px;margin:157px auto;" id="card-window">
        <a-tabs>
          <!-- 登录界面 -->
          <a-tab-pane key="sign in" tab="登录">
            <!-- 登录表单 -->
            <a-form-model ref="loginForm" :model="loginForm" v-bind="layout">
            <a-input placeholder="用户名" style="margin-top:30px">
              <a-icon slot="prefix" type="user" />
            </a-input>
            <a-input-password placeholder="密码" style="margin-top:30px">
              <a-icon slot="prefix" type="info-circle" />
            </a-input-password>
            </a-form-model>
            <a-row type="flex" justify="center" style="margin-top:30px;margin-bottom:30px">
              <a-col :span="11">
                <a-button type="primary" block @click="checklogin()">
                    <div style="color:#000000;">登录</div>
                </a-button>
              </a-col>
            </a-row>
            <img src="../assets/cabbage.png" alt="卷心菜" height="140px" />
          </a-tab-pane>

          <!-- 注册界面 -->
          <a-tab-pane key="sign up" tab="注册" force-render>
            <!-- 注册表单 -->
            <a-form-model ref="ruleForm" :model="ruleForm" :rules="rules" v-bind="layout">
              <a-form-model-item has-feedback prop="email" style="marginBottom:0" :wrapper-col="{span:24}">
                <a-input placeholder="Email" style="margin-top:30px">
                  <a-icon slot="prefix" type="mail" />
                </a-input>
              </a-form-model-item>
              <a-form-model-item has-feedback prop="username" style="marginBottom:0" :wrapper-col="{span:24}">
                <a-input placeholder="用户名" style="margin-top:30px">
                  <a-icon slot="prefix" type="user" />
                </a-input>
              </a-form-model-item>
              <a-form-model-item has-feedback prop="pass" style="marginBottom:0" :wrapper-col="{span:24}">
                <a-input-password placeholder="密码" style="margin-top:30px" autocomplete="off" />
              </a-form-model-item>
              <a-form-model-item has-feedback prop="checkPass" style="marginBottom:0" :wrapper-col="{span:24}">
                <a-input-password placeholder="确认密码" style="margin-top:30px" autocomplete="off" />
              </a-form-model-item>
            </a-form-model>

            <a-row type="flex" justify="center" style="margin-top:30px;margin-bottom:30px">
              <a-col :span="11">
                <a-button type="primary" block @click="checklogin()">
                  <div style="color:#000000;">注册</div>
                  </a-button>
              </a-col>
            </a-row>
          </a-tab-pane>

        </a-tabs>
      </a-card>
    </a-layout-content>
  </a-layout>
</template>

<script>
export default {
  methods:{
    checklogin(){
      this.$router.push("/home");
    }
  }
}
</script>

<style scoped>
#card{
   background: white;
   background-size: cover;
}

#card-window{
    background: black;
}

.ant-tabs-tab-active{
    color: white !important;
}
</style>