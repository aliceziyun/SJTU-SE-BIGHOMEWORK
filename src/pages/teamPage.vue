<template>
  <a-layout>
    <div style="background: white">
      <a-col :span="2">
        <a-input-search
          placeholder="search team"
          style="width: 300px; margin-left: 650px; margin-top: 20px"
        />
      </a-col>

      <a-col :span="14"></a-col>
      <a-col :span="2" :offset="5">
        <a-affix :offset-top="top">
          <a-popover placement="topRight">
            <template slot="content">
              <span style="font-size: 20px">click here to create your GROUP!</span>
            </template>
            <a-button
              type="primary"
              icon="plus"
              size="small"
              block
              @click="shownewteamform"
              style="margin-top: 22px"
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
                <team-collapse :teamObj="item" :fav="0"> </team-collapse>
            </a-list-item>
          </a-list>
        </div>
      </a-card>
      <a-modal
        title="CREATE GROUP"
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
            <a-form-model-item label="groupname">
              <a-input v-model="newteamform.groupname" />
            </a-form-model-item>
            <a-form-model-item label="description">
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
const data = [
];
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
      this.newteam();
    },
    newteam() {
      var _this = this;
      let formData = new FormData();
      formData.append("username", localStorage.getItem("token"));
      formData.append("groupname", this.newteamform.groupname);
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
            _this.successmsg("successful create");
            setTimeout(() => {
              myrefresh();
            }, 2000);
          } else {
            _this.errormsg("create fail,please try again later");
          }
        })
        .catch(function () {
          _this.errormsg("create fail,please try again later");
        });
    },
  },
  mounted() {
    var _this = this;
        let formData = new FormData();
        formData.append('username', localStorage.getItem('token'));
        let config = {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        };
    axios
      .post("http://localhost:5000/api/mygroup/", formData, config)
      .then(function (response) {
        if (response) {
          _this.data = response.data;
        } else {
          alert("please login first!");
        }
      })
  },
};
</script>