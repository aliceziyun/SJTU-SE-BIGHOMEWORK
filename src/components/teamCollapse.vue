<template>
  <div>
    <a-collapse
      :expand-icon-position="expandIconPosition"
      @click="delete_group"
    >
      <a-collapse-panel :header="teamObj.groupname" style="width: 1000px">
        <div>
          <p style="text-align: left; font-size: 15px">
            group description:&#12288;&#12288;{{ teamObj.description }}
          </p>
        </div>
        <div>
          <member-list :prop-groupid="teamObj.groupid"></member-list>
        </div>
        <div style="text-align: left; font-size: 15px">
          <p> group document:&#12288;&#12288; </p>
          <p v-for="(item,index) in group_doc" :key="index">
            &#12288;&#12288;Title:  {{item.title}}&#12288;&#12288;&#12288;&#12288;
            ModifiedTime:  {{moment(item.modifiedTime).format("YYYY-MM-DD")}}
            &#12288;&#12288;&#12288;&#12288;
            <a
              href="#"
              @click="delete_doc(item.id)"
              >delete</a
            >
          </p>
          
        </div>
        <a-icon
          slot="extra"
          type="file-add"
          style="margin-right:10px; fontsize:20px"
          @click="try_add_doc"
        />
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
          @click="showInvite"
        />
        <a-icon
          slot="extra"
          type="setting"
          style="margin-right: 0px; fontsize: 20px"
        />
      </a-collapse-panel>
    </a-collapse>
    <a-modal
      title="invite member to join the group"
      :visible="vis_invite"
      :footer="null"
      @ok="inviteUser"
      @cancel="cancelInvite"
    >
      <template>
        <div>
          <a-input-search
            placeholder="input username"
            enter-button
            @search="onSearch"
          />
          <br /><br />
          <a-table :columns="columns" :data-source="data" rowKey="id">
            <!--<a slot="action" slot-scope="text" href="javascript:;">Delete</a>-->
            <a
              slot="action"
              slot-scope="text"
              href="javascript:;"
              @click="invite(text.id)"
              >Invite</a
            >

            <p slot="expandedRowRender" slot-scope="record" style="margin: 0">
              {{ record.description }}
            </p>
          </a-table>
        </div>
      </template>
    </a-modal>

    <a-modal title="select the document you want to share" :visible="vis_add_doc"
      :footer="null"
      @ok="add_doc"
      @cancel="cancel_add" 
    >
      <a-table :columns="add_doc_columns" :data-source="add_doc_data" rowKey="id">
        <a slot="action" slot-scope="text" href="javascript:;" @click="add_doc(text.id)">Add</a>
      </a-table>
    </a-modal>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
import memberList from "./memberList.vue";
function myrefresh() {
  window.location.reload();
}
const columns = [
  { title: "Name", dataIndex: "username", key: "username" },
  { title: "Email", dataIndex: "email", key: "email" },
  {
    title: "Action",
    dataIndex: "",
    key: "x",
    scopedSlots: { customRender: "action" },
  },
];
const data = [];

const add_doc_columns = [
  { title: "docName", dataIndex: "title", key: "username" },
  {
    title: "Action",
    dataIndex: "",
    key: "x",
    scopedSlots: { customRender: "action" },
  },
];
const add_doc_data = [];
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
      vis_invite: false,
      data,
      columns,
      add_doc_columns,
      add_doc_data,
      vis_add_doc: false,
      my_doc: "",
      group_doc:"",
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
        //   .post(this.$url + "/api/get_user_byid/", formData, config)
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
    var _this = this;
    let formData = new FormData();
    formData.append("groupid", this.teamObj.groupid);
    let config = {
      headers: {
         "Content-Type": "multipart/form-data",
      },
    };
    axios
        .post("http://localhost:5000/api/get_group_doc/", formData, config)
        .then(function (response) {
          if (response) {
            // console.log(response.data)
            _this.group_doc=response.data
            console.log(_this.group_doc[0])
          } else {
            _this.errormsg("invite fail");
          }
        })
        .catch(function (error) {
          console.log("wrong", error);
        });
    
  },

  methods: {
    showInvite() {
      this.vis_invite = true;
    },
    cancelInvite() {
      this.vis_invite = false;
    },
    cancel_add(){
      console.log("cancel");
      this.vis_add_doc = false;
    },
    inviteUser() {
      this.ModalText = "The modal will be closed after two seconds";
      this.confirmLoading = true;
      setTimeout(() => {
        this.vis_invite = false;
        this.confirmLoading = false;
      }, 2000);
    },

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
    add_doc(id){
      console.log(id);
      var _this = this;
      let formData = new FormData();
      formData.append("documentid", id);
      formData.append("groupid", this.teamObj.groupid);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/add_group_doc/", formData, config)
        .then(function (response) {
          if (response) {
            // console.log(response.data)
            if (response.data.message == "success"){
              _this.successmsg("successful add");
              setTimeout(() => {
                myrefresh();
              }, 2000);
            }
            else
              _this.errormsg("document has existed");
          } else {
            _this.errormsg("invite fail");
          }
        })
        .catch(function (error) {
          console.log("wrong", error);
        });
    },
    try_add_doc(){
      var _this = this;
      console.log("添加文档");
      let formData = new FormData();
      formData.append("groupid", this.teamObj.groupid);
      formData.append('username', localStorage.getItem('token'));
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      };
      console.log("hhhh");
      // console.log(formData.get("username"));
      axios
        .post("http://localhost:5000/api/groupiscreatedbyme/", formData, config)
        .then(function (response) {
          // console.log(response)
          if (response) {
            console.log(response.data);
            _this.get_doc();
          } 
          else {
            alert("you are NOT the leader!");
          }
        })
        .catch(function (error) {
          console.log("wrong", error);
        });

    },
    delete_group() {
      // console.log("hhh");
      var _this = this;
      this.$confirm({
        title: <div style="font-weight:bold">CONFIRM DISMISS GROUP?</div>,
        content: (
          <div style="color:red;font-weight:bold">
            <p>the group will be dismissed!</p>
            <p>the doc belonged to the group will be DELETED PERMANENTLY!</p>
          </div>
        ),
        okText: "delete",
        okType: "danger",
        cancelText: "cancel",
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
                _this.successmsg("successful delete");
                setTimeout(() => {
                  myrefresh();
                }, 2000);
              } else {
                _this.errormsg("delete fail,please try again later");
              }
            })
            .catch(function () {
              _this.errormsg("delete fail,please try again later");
            });
        },
      });
    },
    onSearch(value) {
      //   搜索框显示
      console.log(value);
      this.get_user(value);
    },
    get_user(value) {
      var _this = this;
      let formData = new FormData();
      console.log(this.teamObj.groupid);
      formData.append("groupid", this.teamObj.groupid);
      formData.append("keyword", value);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/queryuser/", formData, config)
        .then(function (response) {
          if (response) {
            _this.data = response.data;
            console.log(response.data);
          } else {
            alert("please login!");
          }
        })
        .catch(function (error) {
          console.log("wrong", error);
        });
    },
    invite(id) {
      // console.log(id);
      var _this = this;
      let formData = new FormData();
      formData.append("user_id", id);
      formData.append("group_id", this.teamObj.groupid);
      formData.append("groupname", this.teamObj.groupname);
      formData.append("leader_username", localStorage.getItem("token"));

      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/invite_user/", formData, config)
        .then(function (response) {
          if (response) {
            _this.successmsg("successful invite");
            setTimeout(() => {
              myrefresh();
            }, 2000);
          } else {
            _this.errormsg("invite fail");
          }
        })
        .catch(function (error) {
          console.log("wrong", error);
        });
    },
    get_doc(){
      var _this = this;
      let formData = new FormData();
      console.log(this.teamObj.groupid);
      formData.append('username', localStorage.getItem('token'));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/my_docs/", formData, config)
        .then(function (response) {
          if (response) {
            console.log(response.data);
            _this.add_doc_data = response.data;
            _this.vis_add_doc = true;
            console.log("hhh");
          } else {
            _this.errormsg("search failed");
          }
        })
        .catch(function (error) {
          console.log("wrong", error);
        });
    },
    delete_doc(id){
      var _this = this;
      let formData = new FormData();
      formData.append('documentid', id);
      formData.append("groupid", this.teamObj.groupid);
      let config = {
        headers: {
          "Content_Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/delete_group_doc/", formData, config)
        .then(function(response) {
          if(response) {
            console.log(response);
            if (response.data.message=="success")
            _this.successmsg("successful delete");
            setTimeout(() => {
              myrefresh();
            }, 1000);
          } else{
            _this.errormsg("delete failed");
          }
        })
        .catch(function(error) {
          console.log("wrong", error);
        });
    },
  },
};
</script>
