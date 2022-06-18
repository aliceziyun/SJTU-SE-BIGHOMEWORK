<template>
  <div class="home" v-title data-title="请开始编辑你的文档！">
    <a-layout id="components-layout-demo-top-side-2">
      <a-layout>
        <a-layout-sider width="300" style="background: #fff">
          <a-tabs type="card" @change="callback">
            <a-tab-pane key="1" tab="comment" :disabled="!discuss_right">
              <div style="margin-left: 5px; margin-right: 5px">
                <a-input-search
                  placeholder="input your comment"
                  v-model="keyword"
                  enter-button="comment"
                  @search="newComment"
                />
              </div>
              <a-list
                class="comment-list"
                item-layout="horizontal"
                :data-source="comment"
              >
                <a-list-item
                  slot="renderItem"
                  slot-scope="item"
                  style="height: 70px; float: left"
                >
                  <memberAvatar :username="item.username"></memberAvatar>
                  <a-comment style="margin-right: 10px; width: 200px">
                    <p align="left" slot="content">{{ item.content }}</p>
                    <a-tooltip
                      slot="datetime"
                      :title="
                        moment(item.datetime)
                          .subtract(8, 'hours')
                          .format('YYYY-MM-DD HH:mm:ss')
                      "
                    >
                      <span>{{
                        moment(item.datetime).subtract(8, "hours").fromNow()
                      }}</span>
                    </a-tooltip>
                  </a-comment>
                </a-list-item>
              </a-list>
            </a-tab-pane>
            <a-tab-pane key="2" tab="history">
              <a-list
                class="comment-list"
                item-layout="horizontal"
                :data-source="modify_history"
              >
                <a-list-item
                  slot="renderItem"
                  slot-scope="item"
                  style="height: 70px; float: left"
                >
                        <a-button
                        id="memory-btn"
                        @click="
                          memory(
                            moment(item.datetime)
                              .subtract(8, 'hours')
                              .format('YYYY-MM-DD HH:mm:ss')
                          )
                        "
                        >BACK</a-button
                      >
                  <memberAvatar :username="item.username"></memberAvatar>
                  <a-comment style="margin-right: 10px; width: 200px">
                    <p align="left" slot="content">{{ item.content }}</p>
                    <a-tooltip
                      slot="datetime"
                      :title="
                        moment(item.datetime)
                          .subtract(8, 'hours')
                          .format('YYYY-MM-DD HH:mm:ss')
                      "
                    >
                      <span>{{
                        moment(item.datetime).subtract(8, "hours").fromNow()
                      }}</span>
                    </a-tooltip>
                  </a-comment>
                </a-list-item>
              </a-list>
            </a-tab-pane>
            <a-tab-pane key="3" tab="share" :disabled="!share_right">
              <a-input placeholder="user" v-model="inviteuser" />
              <a-button
                type="primary"
                block
                style="margin-top:10px;margin-bottom=10px"
                @click="searchuser"
                >search users</a-button
              >
              <a-table
                rowKey="id"
                v-show="invitedata != null"
                :columns="inviteColumns"
                :data-source="invitedata"
                size="small"
              >
                <a
                  slot="action"
                  slot-scope="text"
                  href="javascript:;"
                  @click="invite(text.id)"
                  >Share</a
                >
              </a-table>
            </a-tab-pane>

            <a-tab-pane key="4" tab="manage right">
              <div style="margin-left: 10px; margin-right: 10px">
                <privilege-pane
                  :propRightObj="this.rights"
                  :propDocumentID="this.$route.params.id"
                ></privilege-pane>
              </div>
            </a-tab-pane>
          </a-tabs>
        </a-layout-sider>
        <a-layout style="padding: 0 24px 24px">
          <a-breadcrumb style="margin: 16px 0; text-align: left">
            <a-breadcrumb-item>文档 </a-breadcrumb-item>
            <a-breadcrumb-item>{{ DOCtitle }}</a-breadcrumb-item>
            <a-breadcrumb-item>
              <a @click="BacktoNext()"><i class="fa fa-arrow-left"></i></a>
            </a-breadcrumb-item>
          </a-breadcrumb>
          <a-row style="margin-bottom: 10px">
            <span style="float: left; margin-top: 10px">editing</span>
            <span
              v-for="(user, index) in userList"
              :key="index"
              style="float: left"
            >
              <memberAvatar
                :username="user.username"
                style="float: right"
              ></memberAvatar>
            </span>
          </a-row>
          <a-layout-content
            :style="{
              background: '#fff',
              padding: '24px',
              margin: 0,
              minHeight: '280px',
            }"
          >
            <mavon-editor
              v-model="content"
              ref="md"
              @change="change"
              style="min-height: 600px; z-index: 1"
              :editable="modify_right"
              @save="save_docs()"
            />
          </a-layout-content>
          <a-button @click="getPdf()"
            ><a-icon type="download" size="small" />import as pdf</a-button
          >
          <a-button @click="exportWord()"
            ><a-icon type="download" />import as word</a-button
          >
        </a-layout>
      </a-layout>
    </a-layout>
  </div>
</template>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="https://cdn.bootcss.com/jspdf/1.3.4/jspdf.debug.js"></script>

<script>
import { mavonEditor } from "mavon-editor";
import "mavon-editor/dist/css/index.css";
import axios from "axios";
import moment from "moment";
import "@/utils/htmlToPdf.js";
import docxtemplater from "docxtemplater";
import PizZip from "pizzip";
import JSZipUtils from "jszip-utils";
import { saveAs } from "file-saver";
import privilegePane from "../components/privilegePane.vue";
import memberAvatar from "../components/memberAvatar";
import $ from "jquery";
import html2canvas from "html2canvas";
const inviteColumns = [
  {
    title: "Email",
    dataIndex: "email",
    key: "email",
  },
  {
    title: "Username",
    dataIndex: "username",
    key: "username",
  },
  {
    title: "Action",
    dataIndex: "",
    key: "x",
    scopedSlots: {
      customRender: "action",
    },
  },
];
function myrefresh() {
  window.location.reload();
}
function contains(arr, obj) {
  var i = arr.length;
  while (i--) {
    if (arr[i].username === obj) {
      return true;
    }
  }
  return false;
}
export default {
  name: "Home",
  components: {
    mavonEditor,
    memberAvatar,
    privilegePane,
  },
  data() {
    return {
      htmlTitle: "导出文件",
      timer: "",
      userList: [],
      inviteuser: "",
      inviteColumns,
      invitedata: [],
      form: {
        content: "",
        username: "",
        title: "",
      },
      content: "",
      sendjson: {
        content: "",
        username: "",
      },
      html: "",
      configs: {},
      collapsed: false,
      moment,
      keyword: "",
      comment: [],
      modify_history: [],
      watch_right: false,
      modify_right: true,
      discuss_right: true,
      share_right: true,
      userId: 0,
      doctitle: "",
      rights: {},
    };
  },
  methods: {
    exportReport() {
      exportReportTemplet();
    },
    exportWord: function () {
      let _this = this;
      console.log(_this.form);
      JSZipUtils.getBinaryContent("/template.docx", function (error, content) {
        if (error) {
          console.log(error);
          throw error;
        }

        let zip = new PizZip(content);
        let doc = new docxtemplater().loadZip(zip);
        doc.setData(_this.form);

        try {
          doc.render();
        } catch (error) {
          let e = {
            message: error.message,
            name: error.name,
            stack: error.stack,
            properties: error.properties,
          };
          console.log(JSON.stringify({ error: e }));
          throw error;
        }
        let out = doc.getZip().generate({
          type: "blob",
          mimeType:
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        });
        saveAs(out, "Docs.docx");
      });
    },
    change(value, render) {
      this.html = render;
    },
    successmsg(message) {
      this.$message.success(message);
    },
    errormsg(message) {
      this.$message.error(message);
    },
    warningmsg(message) {
      this.$message.warning(message);
    },
    load_right(id) {
      let formData = new FormData();
      formData.append("DocumentID", id);
      formData.append("username", localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      var _this = this;
      axios
        .post("http://localhost:5000/api/tell_doc_right/", formData, config)
        .then(function (response) {
          if (response) {
            console.log(response.data);
            _this.rights = response.data;
            console.log("loading rights", _this.rights);
            if (response.data.usertype == 0) {
              _this.watch_right = response.data.others_watch_right;
              _this.modify_right = response.data.others_modify_right;
              _this.discuss_right = response.data.others_discuss_right;
              _this.share_right = response.data.others_share_right;
            } else {
              _this.watch_right = response.data.watch_right;
              _this.modify_right = response.data.modify_right;
              _this.discuss_right = response.data.discuss_right;
              _this.share_right = response.data.share_right;
            }
            {
              _this.load_data(_this.$route.params.id);
              if (_this.discuss_right == true) {
                _this.load_comment(_this.$route.params.id);
              }
              _this.load_modify_history(_this.$route.params.id);
              _this.userList.push({
                username: localStorage.getItem("token"),
              });
              _this.initWebSocket();
            }
          }
        })
        .catch(function (error) {
          console.log("Fail", error);
        });
    },
    searchuser() {
      var _this = this;
      let formData = new FormData();
      formData.append("keyword", _this.inviteuser);
      formData.append("document_id", _this.$route.params.id);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post(
          "http://localhost:5000/api/query_notindoc_user/",
          formData,
          config
        )
        .then(function (response) {
          if (response.data != null) {
            console.log(response.data);
            _this.invitedata = response.data;
          } else {
            _this.errormsg("查找失败，请尝试刷新后再次创建");
          }
        })
        .catch(function () {
          _this.errormsg("查找失败，请尝试刷新后再次创建");
        });
    },
    invite(e) {
      var _this = this;
      let formData = new FormData();
      formData.append("user_id", this.userId);
      formData.append("DocumentID", _this.$route.params.id);
      formData.append("target_user_id", e);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post(
          "http://localhost:5000/api/pernal_doc_share_to/",
          formData,
          config
        )
        .then(function (response) {
          if (response) {
            _this.successmsg("邀请成功");
          } else {
            _this.errormsg("邀请失败");
          }
        })
    },

    callback() {},
    save_docs() {
      var _this = this;
      let formData = new FormData();
      formData.append("content", this.content);
      formData.append("DocumentID", this.$route.params.id);
      formData.append("username", localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/modify_doc/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
            _this.successmsg("保存成功");
            _this.$router.push("/editor/" + response.data.id);
            myrefresh();
          }
        })
    },
    newComment() {
      this.comment.unshift({
        content: this.keyword,
        username: localStorage.getItem("token"),
        datetime: moment().add(8, "hours"),
      });
      console.log(moment().add(8, "hours").calendar());
      let formData = new FormData();
      formData.append("DocumentID", this.$route.params.id);
      formData.append("username", localStorage.getItem("token"));
      formData.append("content", this.keyword);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/create_comment/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
          }
        })
      this.keyword = "";
    },
    memory(time) {
      let formData = new FormData();
      formData.append("time", time);
      formData.append("DocumentID", this.$route.params.id);
      formData.append("username", localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      var _this = this;
      axios
        .post("http://localhost:5000/api/memory_back/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
            _this.$router.push("/editor/" + response.data.id);
            myrefresh();
          }
        })
    },
    load_data(id) {
      let formData = new FormData();
      formData.append("DocumentID", id);
      formData.append("username", localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      var _this = this;
      axios
        .post("http://localhost:5000/api/get_doccontent/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
            _this.content = response.data.content;
            _this.form.content = response.data.content;
            _this.form.username = localStorage.getItem("token");
          }
        })
    },
    load_comment(id) {
      let formData = new FormData();
      formData.append("DocumentID", id);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };id
      var _this = this;
      axios
        .post(
          "http://localhost:5000/api/get_all_comment/",
          formData,
          config
        )
        .then(function (response) {
          if (response) {
            _this.comment = response.data;
          }
        })
    },
    load_modify_history(id) {
      let formData = new FormData();
      formData.append("DocumentID", id);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      var _this = this;
      axios
        .post(
          "http://localhost:5000/api/get_all_modified_time/",
          formData,
          config
        )
        .then(function (response) {
          if (response) {
            _this.modify_history = response.data;
          }
        })
    },
    initWebSocket() {
      const wsuri = "ws://192.168.1.112:8888/conn";
      this.websock = new WebSocket(wsuri);
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onopen = this.websocketonopen;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
    },
    websocketonopen() {
      console.log("连接成功");
    },
    sendcontent() {
      console.log("sendmessage");
      this.sendjson.content = this.content;
      this.sendjson.username = localStorage.getItem("token");
      this.websocketsend(JSON.stringify(this.sendjson));
    },
    websocketonerror() {
      this.initWebSocket();
    },
    websocketonmessage(e) {
      var jsondata = JSON.parse(
        e.data.replace(/\n/g, "\\n").replace(/\r/g, "\\r")
      );
      this.content = jsondata.content;
      if (contains(this.userList, jsondata.username)) {
      } else {
        var tmp = {
          username: jsondata.username,
        };
        this.userList.push(tmp);
      }
    },
    websocketsend(Data) {
      this.websock.send(Data);
    },
    websocketclose() {
      console.log("断开连接");
    },
    BacktoNext() {
      this.$router.push("/home");
    },
    load_id() {
      let formData1 = new FormData();
      var _this = this;
      formData1.append("username", localStorage.getItem("token"));
      let config1 = {
        headers: {
          "Content-Type": "multipart/form-data1",
        },
      };
      axios
        .post("http://localhost:5000/api/get_user/", formData1, config1)
        .then(function (response) {
          if (response) {
            _this.userId = response.data.id;
          } else {
            _this.errormsg("获取用户ID失败");
          }
        })
    },
    load_title(id) {
      let formData1 = new FormData();
      var _this = this;
      formData1.append("username", localStorage.getItem("token"));
      formData1.append("DocumentID", id);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/get_doctitle/", formData1, config)
        .then(function (response) {
          if (response) {
            _this.doctitle = response.data.title;
            _this.form.title = _this.doctitle;
          }
        })
    },
  },

  destroyed() {
    clearInterval(this.timer);
    this.websock.close(); 
  },
  mounted: function () {
    this.load_title(this.$route.params.id);
    this.load_right(this.$route.params.id);
    this.load_id();
  },
  computed: {
    DOCtitle() {
      return this.doctitle;
    },
    DOCcontent() {
      return this.content;
    },
  },
  watch: {
    content() {
      this.sendcontent();
    },
  },
};
</script>
<style>
#components-layout-demo-side .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}

#memory-btn {
  height: 20px;
  width: 50px;
  font-size: 5%;
  margin-left: 10px;
  margin-top: 0px;
}
</style>