<template>
  <a-layout>
    <div style="background: white">
      <a-col :span="2">
        <a-input-search
          placeholder="查询团队"
          style="width: 300px; margin-left: 20px; margin-top: 20px"
        />
      </a-col>

      <a-col :span="14"></a-col>
      <a-col :span="2" :offset="5">
        <a-affix :offset-top="top">
          <a-popover placement="topRight">
            <template slot="content">
              <span style="font-size: 10px">点击创建一个属于你的团队! QvQ</span>
            </template>
            <a-button
              type="primary"
              icon="plus"
              size="large"
              block
              @click="shownewteamform"
              style="margin-top: 10px"
            ></a-button>
          </a-popover>
        </a-affix>
      </a-col>
    </div>

    <a-layout-content style="background: white">
      <a-card style="width: 1200px; height: 500px; margin: 50px auto">
        <div>
          <a-list :data-source="data">
            <a-list-item slot="renderItem" slot-scope="item">
              <a-collapse :expand-icon-position="expandIconPosition">
                <team-collapse :teamObj="item" :fav="0"> </team-collapse
              ></a-collapse>
            </a-list-item>
          </a-list>
        </div>
      </a-card>
      <a-modal
        title="创建团队"
        :visible="newteamvisible"
        @ok="createteam"
        @cancel="cancelcreate"
      >
        <template>
          <a-form-model
            :model="newteamform"
            :label-col="labelCol"
            :wrapper-col="wrapperCol"
          >
            <a-form-model-item label="团队队名">
              <a-input v-model="newteamform.groupname" />
            </a-form-model-item>
            <a-form-model-item label="团队简介">
              <a-input v-model="newteamform.description" />
            </a-form-model-item>
          </a-form-model>
        </template>
      </a-modal>
    </a-layout-content>
  </a-layout>
</template>

<style>
#team-title {
  font-size: 40px;
  color: black;
}
</style>

<script>
import axios from "axios";
import TeamCollapse from "../components/teamCollapse.vue";
const data = [];
function myrefresh() {
  window.location.reload();
}
export default {
  components: {
    TeamCollapse,
  },
  data() {
    return {
      text: "还没整，不急哈",
      newteamvisible: false,
      newteamform: {
        groupname: "",
        description: "",
      },
      data,
    };
  },
  methods: {
    successmsg(message) {
      this.$message.success(message);
    },
    errormsg(message) {
      this.$message.error(message);
    },
    cancelcreate() {
      this.newteamvisible = false;
    },
    shownewteamform() {
      this.newteamvisible = true;
    },
    createteam() {
      // this.checkedList.forEach(element => {
      //   if(element=="修改")this.newteamform.modify_right=1;
      //   if(element=="评论")this.newteamform.discuss_right=1;
      //   if(element=="分享")this.newteamform.share_right=1;
      // });

      this.newteam();
    },
    newteam() {
      var _this = this;
      let formData = new FormData();
      formData.append("username", localStorage.getItem("token"));
      formData.append("groupname", this.newteamform.groupname);
      // formData.append("modify_right", this.newdocform.modify_right);
      // formData.append("share_right", this.newdocform.share_right);
      // formData.append("discuss_right", this.newdocform.discuss_right);
      formData.append("description", this.newteamform.description);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };

      axios
        .post("http://localhost:5000/api/creategroup/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
            _this.successmsg("创建成功");
            setTimeout(() => {
              myrefresh();
            }, 2000);
          } else {
            _this.errormsg("创建失败，请尝试刷新后再次创建");
          }
        })
        .catch(function () {
          _this.errormsg("创建失败，请尝试刷新后再次创建");
        });
    },
  },
  get_my_founded_teams() {
    var _this = this;
    let formData = new FormData();
    formData.append("username", localStorage.getItem("token"));
    let config = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };
    axios
      .post("http://localhost:5000/api/group_created_byme/", formData, config)
      .then(function (response) {
        if (response) {
          _this.data = response.data;
          console.log("创建团队列表加载完成1");
          console.log(response);
          console.log("创建团队列表加载完成2");
        } else {
          alert("请先登录！");
        }
      })
      .catch(function (error) {
        console.log("wrong", error);
      });
  },
  load_userId() {
    this.userId = localStorage.getItem("token");
  },
  mounted() {
    this.load_userId();
    get_my_founded_teams();
  },
};
</script>
