<template>
  <div>
    <a-card hoverable style="width: 190px" :title="docObj.title" align="center">
      <img
        slot="cover"
        alt="example"
        :src="imgsrc"
        @click="toDocs(docObj.id)"
      />
      <template slot="actions">
        <a-tooltip placement="bottom" v-if="fav == 0">
          <template slot="title">
            <span>move to bin</span>
          </template>
          <a-icon type="delete" @click="confirmDelete(1)" />
        </a-tooltip>
        <a-tooltip placement="bottom" v-if="fav == 0">
          <template slot="title">
            <span>edit title</span>
          </template>
          <a-icon type="edit" @click="showModal()" />
        </a-tooltip>
        <a-tooltip placement="bottom" v-if="fav == 0">
          <template slot="title">
            <span>share doc</span>
          </template>
          <a-icon type="share-alt" @click="shareDocForm()" />
        </a-tooltip>

        <a-tooltip placement="bottom" v-if="fav == 1">
          <template slot="title">
            <span>move to bin</span>
          </template>
          <a-icon type="delete" @click="confirmDelete(1)" />
        </a-tooltip>
        <a-tooltip placement="bottom" v-if="fav == 1">
          <template slot="title">
            <span>edit title</span>
          </template>
          <a-icon type="edit" @click="showModal()" />
        </a-tooltip>
        <a-tooltip placement="bottom" v-if="fav == 1">
          <template slot="title">
            <span>?</span>
          </template>
          <a-icon type="share-alt" @click="shareDocForm()" />
        </a-tooltip>

        <a-tooltip placement="bottom" v-if="fav == 2">
          <template slot="title">
            <span>move to bin</span>
          </template>
          <a-icon type="delete" @click="confirmDelete(1)" />
        </a-tooltip>
        <a-tooltip placement="bottom" v-if="fav == 2">
          <template slot="title">
            <span>edit title</span>
          </template>
          <a-icon type="edit" @click="showModal()" />
        </a-tooltip>
        <a-tooltip placement="bottom" v-if="fav == 2">
          <template slot="title">
            <span>share doc</span>
          </template>
          <a-icon type="share-alt" @click="shareDocForm()" v-if="fav == 2" />
        </a-tooltip>

        <!-- <a-tooltip placement="bottom" v-if="fav==3">
        <template slot="title">
          <span>移到回收站</span>
        </template>
        <a-icon type="delete" @click="confirmDelete(1)" v-if="fav==3"/>
        </a-tooltip>
        <a-tooltip placement="bottom" v-if="fav==3">
        <template slot="title">
          <span>修改标题</span>
        </template>
        <a-icon type="edit" @click="showModal()" v-if="fav==3"/>
        </a-tooltip>
        <a-tooltip placement="bottom" v-if="fav==3">
        <template slot="title">
          <span>收藏文档</span>
        </template>
        <a-icon type="file-add" @click="addFavorDocs()" v-if="fav==3" />
        </a-tooltip> -->

        <a-tooltip placement="bottom" v-if="fav == 4">
          <template slot="title">
            <span>restore doc</span>
          </template>
          <a-icon
            type="unlock"
            @click="revoverDoc(docObj.id)"
            v-if="fav == 4"
          />
        </a-tooltip>
        <a-tooltip placement="bottom" v-if="fav == 4">
          <template slot="title">
            <span>delete file permanently</span>
          </template>
          <a-icon type="delete" @click="confirmDelete(2)" v-if="fav == 4" />
        </a-tooltip>

        <!--<a-icon type="delete" @click="confirmDelete(1)" v-if="fav!=2"/>
        <a-icon type="unlock" @click="revoverDoc()" v-if="fav==2"/>
        <a-icon type="edit" @click="showModal()" v-if="fav!=2"/>
        <a-icon type="delete" @click="confirmDelete(2)" v-if="fav==2"/>
        <a-icon type="file-add" @click="addFavorDocs()" v-if="fav==0" />
        <a-icon type="minus-square" @click="delFavorDocs()" v-if="fav==1" />-->
      </template>
      <span> owner:{{ this.username }}</span>
      <br /><br />
      <span>
        date:{{ moment(docObj.created_time).format("YYYY-MM-DD") }}</span
      >
    </a-card>

    <a-modal
      title="SHARE DOC"
      :visible="sharevisible"
      @ok="shareDoc(shareEmail,docObj.id)"
      @cancel="cancelshare"
    >
    <template>
        <a-input v-model="shareEmail" placeholder="Please input the email of the user and we will send invitation" />
    </template>
    </a-modal>

    <a-modal
      title="EDIT DOC TITLE"
      :visible="visible"
      @ok="handleOk"
      @cancel="handleCancel"
    >
      <template>
        <a-form-model
          :model="form"
          :label-col="labelCol"
          :wrapper-col="wrapperCol"
        >
          <a-form-model-item label="Doc Title">
            <a-input v-model="form.title" />
          </a-form-model-item>
        </a-form-model>
      </template>
    </a-modal>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";

function myrefresh() {
  window.location.reload();
}
export default {
  name: "docCard",

  props: {
    docObj: {
      id: { type: Number, dafault: 0 },
      title: { type: String, default: "" },
      created_time: { type: String, default: "" },
      creator_id: {type: Number, default: 0},
    },
    fav: {
      type: Number,
    },
  },

  data() {
    return {
      form: {
        DocumentID: "",
        title: "",
        fav: "",
        creator_id: "",
      },
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      visible: false,
      creator_id: "",
      group_id: "",
      moment,
      username: "",
      shareEmail:"",
      sharevisible: false,
      imgsrc:"",
    };
  },

  watch: {
    docObj: {
      handler(newVal) {
        this.form.DocumentID = newVal.id;
        this.form.title = newVal.title;
        this.form.creator_id = newVal.creator_id; // 文档的创建者
        this.form.group_id = newVal.group_id; // 文档所属的组
        this.group_id = newVal.group_id;
        var _this = this;
        let formData = new FormData();
        formData.append("userid", this.form.creator_id);
        let config = {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        };
        axios
          .post("http://localhost:5000/api/get_user_byid/", formData, config)
          .then(function (response) {
            if (response) {
              _this.username = response.data.username;
            } else {
              _this.errormsg("retore fail,please try again later");
            }
          })
          .catch(function () {
            _this.errormsg("retore fail,please try again later");
          });
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
    if(this.docObj.creator_id==localStorage.getItem("userid")){
      this.imgsrc = require("../assets/cabbage3.jpg")
    }
    else{
      this.imgsrc = require("../assets/cabbage5.png")
    }
    console.log(this.imgsrc)
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
      this.$router.push("/editor/" + id);
    },
    shareDocForm() {
      this.sharevisible = true;
    },
    cancelshare() {
      this.sharevisible = false;
    },
    deleteDocs(flag, self) {
      console.log("delete" + self.form.DocumentID);
      let formData = new FormData();
      formData.append("DocumentID", self.form.DocumentID);
      formData.append("username", localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      if (flag == 1) {
        axios
          .post("http://localhost:5000/api/recycle_doc/", formData, config)
          .then(function (response) {
            console.log(response.data.message);
            if (response.data.message == "success") {
              self.successmsg("successful delete");
              setTimeout(() => {
                myrefresh();
              }, 2000);
            } else {
              self.errormsg("delete fail,please try again later");
            }
          })
          .catch(function () {
            self.errormsg("delete fail,please try again later");
          });
      } else {
        axios
          .post("http://localhost:5000/api/del_doc/", formData, config)
          .then(function (response) {
            console.log(response.data.message);
            if (response.data.message == "success") {
              self.successmsg("permanently delete");
              setTimeout(() => {
                myrefresh();
              }, 2000);
            } else {
              self.errormsg("delete fail,please try again later");
            }
          })
          .catch(function () {
            self.errormsg("delete fail,please try again later");
          });
      }
    },

    confirmDelete(x) {
      var _this = this;
      // console.log("文档创建者id" + this.form.creator_id);
      // console.log("登录id " + localStorage.getItem("userid"));
      if (this.form.creator_id != localStorage.getItem("userid")) {
        this.errormsg("you don't have the right to delete");
        return;
      }
      this.$confirm({
        title: <div style="font-weight:bold">CONFIRM DELETE?</div>,
        content:
          x == 1 ? (
            <div style="color:red;">the doc will be moved to bin.</div>
          ) : (
            <div style="color:red;">
              the doc will be<span style="font-weight:bold"> PERMANENTLY DELETED!</span>
            </div>
          ),
        okText: "Delete",
        okType: "danger",
        cancelText: "cancel",
        onOk() {
          console.log("OK");
          _this.$options.methods.deleteDocs(x, _this);
        },
        onCancel() {
          console.log("Cancel");
        },
      });
    },

    addFavorDocs() {
      console.log("收藏该项" + this.form.DocumentID);
      var _this = this;
      let formData = new FormData();
      formData.append("DocumentID", this.form.DocumentID);
      console.log(this.form);
      formData.append("username", localStorage.getItem("token"));
      console.log(localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/favor_doc/", formData, config)
        .then(function (response) {
          console.log(response.data.message);
          if (response.data.message == "success") {
            _this.successmsg("收藏成功");
          } else {
            _this.errormsg("您已经收藏过改文档了哦");
          }
        })
        .catch(function () {
          _this.errormsg("收藏失败，请尝试刷新后重试");
        });
    },
    delFavorDocs() {
      console.log("取消收藏该项" + this.form.DocumentID);
      var _this = this;
      let formData = new FormData();
      formData.append("DocumentID", this.form.DocumentID);
      console.log(this.form);
      formData.append("username", localStorage.getItem("token"));
      console.log(localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/cancel_favor_doc/", formData, config)
        .then(function (response) {
          console.log(response.data.message);
          if (response.data.message == "success") {
            _this.successmsg("取消收藏成功");
            setTimeout(() => {
              myrefresh();
            }, 2000);
          } else {
            _this.errormsg("取消收藏失败，请尝试刷新后重试");
          }
        })
        .catch(function () {
          _this.errormsg("取消收藏失败，请尝试刷新后重试");
        });
    },
    revoverDoc(id) {
      var _this = this;
      let formData = new FormData();
      formData.append("DocumentID", id);
      console.log("DocumentId " + id);
      formData.append("username", localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/recover_doc/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
            _this.successmsg("successful restore");
            setTimeout(() => {
              myrefresh();
            }, 2000);
          } else {
            _this.errormsg("restore fail,please try later");
          }
        })
        .catch(function () {
          _this.errormsg("restore fail,please try later");
        });
    },
    showModal() {
      if (this.form.creator_id != localStorage.getItem("userid")) {
        this.errormsg("you don't have the right");
        return;
      }
      this.form.title = this.docObj.title;
      this.form.DocumentID = this.docObj.id;
      this.visible = true;
    },
    shareDoc(email,id){
      var _this = this;
      let formData = new FormData();
      formData.append("DocumentID", id);
      formData.append("username", localStorage.getItem("token"));
      formData.append("Email", email);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/pernal_doc_share_to/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
            _this.successmsg("successful share");
            setTimeout(() => {
              myrefresh();
            }, 2000);
          } else {
            _this.errormsg("share doc fail!");
          }
        })
        .catch(function () {
          _this.errormsg("share fail,please try later!");
        });
    },
    handleOk() {
      if (this.form.creator_id != localStorage.getItem("userid")) {
        this.errormsg("you're not the owner,can't modify the doc!");
        return;
      }
      var _this = this;
      let formData = new FormData();
      formData.append("DocumentID", this.form.DocumentID);
      formData.append("title", this.form.title);
      formData.append("username", localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/modify_doc_basic/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
            _this.successmsg("successful modify");
            setTimeout(() => {
              myrefresh();
            }, 2000);
          } else {
            _this.errormsg("modify fail,you're not the doc owner!");
          }
        })
        .catch(function () {
          _this.errormsg("modify fail,please try later");
        });
    },
    handleCancel() {
      this.visible = false;
    },
  },
};
</script>
