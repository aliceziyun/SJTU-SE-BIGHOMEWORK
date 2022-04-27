<template>
  <a-collapse :expand-icon-position="expandIconPosition" @click="delete_group">
    <a-collapse-panel :header="teamObj.groupname" style="width: 1000px">
      <div>
        <member-list :prop-groupid="teamObj.groupid"></member-list>
      </div>
      <a-icon
        slot="extra"
        type="delete"
        style="margin-right: 10px; fontsize: 20px"
        @click="delete_group"
      />
      <a-icon
        slot="extra"
        type="plus"
        style="margin-right: 10px; fontsize: 20px"
      />
      <a-icon
        slot="extra"
        type="setting"
        style="margin-right: 0px; fontsize: 20px"
      />
    </a-collapse-panel>
  </a-collapse>
</template>

<script>
import axios from "axios";
import moment from "moment";
import memberList from "./memberList.vue";
function myrefresh() {
  window.location.reload();
}
export default {
  name: "teamCollapse",
  components: { memberList },
  props: {
    teamObj: {
      groupid: { type: Number, dafault: 0 },
      groupname: { type: String, default: "" },
      createdtime: { type: String, default: "" },
    },
    fav: {
      type: Number,
    },
  },

  data() {
    return {
      form: {
        GroupID: "",
        groupname: "",
        leaderid: "",
        createdtime: "",
      },
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      visible: false,
      description: "",
      moment,
      username: "",
    };
  },

  watch: {
    teamObj: {
      handler(newVal) {
        this.form.GroupID = newVal.id;
        this.form.groupname = newVal.groupname;
        this.form.createdtime = newVal.createdtime;
        this.form.leaderid = newVal.leaderid;
        this.description = newVal.description;
        // var _this = this;
        // let formData = new FormData();
        // formData.append("userid", this.form.creator_id);
        // let config = {
        //   headers: {
        //     "Content-Type": "multipart/form-data",
        //   },
        // };
        // axios
        //   .post("http://localhost:5000/api/get_user_byid/", formData, config)
        //   .then(function (response) {
        //     if (response) {
        //       _this.username = response.data.username;
        //     } else {
        //       _this.errormsg("恢复失败，请稍后重试");
        //     }
        //   })
        //   .catch(function () {
        //     _this.errormsg("恢复失败，请稍后重试");
        //   });
      },
      deep: true,
      immediate: true,
    },
    fav: {
      handler(newVal) {
        this.form.fav = newVal.fav;
      },
      deep: true,
      immediate: true,
    },
  },
  mounted: function () {
    console.log(this.teamObj.groupid);
  },

  methods: {
    successmsg(message) {
      this.$message.success(message);
    },
    errormsg(message) {
      this.$message.error(message);
    },
    toDocs(id) {
      //这边判断是否能看，比如occupied
      this.$router.push("/docs2/" + id);
    },
    delete_group() {
      // console.log("hhh");
      var _this = this;
      this.$confirm({
        title: <div style="font-weight:bold">确认解散团队？</div>,
        content: (
          <div style="color:red;font-weight:bold">
            <p>团队将被解散！</p>
            <p>团队文档将会 永 远 消 失 ！</p>
          </div>
        ),
        okText: "删除",
        okType: "danger",
        cancelText: "取消",
        onOk() {
          console.log("删除该项" + _this.teamObj.groupid);
          let formData = new FormData();
          formData.append("groupid", _this.teamObj.groupid);
          console.log(localStorage.getItem("token"));
          let config = {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          };
          axios
            .post("http://localhost:5000/api/delete_group/", formData, config)
            .then(function (response) {
              console.log(response.data.message);
              if (response.data.message == "success") {
                _this.successmsg("删除成功");
                setTimeout(() => {
                  myrefresh();
                }, 2000);
              } else {
                _this.errormsg("删除失败，请尝试刷新后重试");
              }
            })
            .catch(function () {
              _this.errormsg("删除失败，请尝试刷新后重试");
            });
        },
      });
    },
  },
};
</script>
