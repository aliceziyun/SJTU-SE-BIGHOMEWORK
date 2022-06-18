<template>
  <div>
    <a-row>
      <a-col :span="10" :offset="7"></a-col>
      <a-col :span="2" :offset="5">
        <a-affix :offset-top="top">
          <a-popover placement="topRight">
            <template slot="content">
              <span style="font-size:20px">click here to create your DOC! :)</span>
            </template>
            <a-button type="primary" icon="plus" size="small" block @click="shownewdocform"></a-button>
          </a-popover>
        </a-affix>
      </a-col>
    </a-row>

    <a-list :grid="{ gutter: 25, xs: 1, sm: 2, md: 4, lg: 4, xl: 6, xxl: 6 }" :data-source="data">
      <a-list-item slot="renderItem" slot-scope="item">
        <docCard :docObj="item" :fav="0"></docCard>
      </a-list-item>
    </a-list>
    <div>
      <a-modal title="CREATE DOC" :visible="newdocvisible" @ok="createdoc" @cancel="cancelcreate">
        <template>
          <a-form-model :model="newdocform" :label-col="labelCol" :wrapper-col="wrapperCol">
            <a-form-model-item label="TITLE">
              <a-input v-model="newdocform.title" />
            </a-form-model-item>
            <a-form-model-item label="RIGHTS">
              <div>
                <div :style="{ borderBottom: '1px solid #E9E9E9' }">
                  <a-checkbox
                    :indeterminate="indeterminate"
                    :checked="checkAll"
                    @change="onCheckAllChange"
                  >Check all</a-checkbox>
                </div>
                <a-checkbox-group v-model="checkedList" :options="plainOptions" @change="onChange" />
              </div>
            </a-form-model-item>
            <a-form-model-item label="TEMPLATE">
              <div>
                <a-radio-group v-model="templateValue" @change="onChangeTem">
                  <a-radio :value="1">empty doc
                  </a-radio>
                  <a-radio :value="2">template 1
                  </a-radio>
                  <a-radio :value="3">template 2
                  </a-radio>
                  
                </a-radio-group>
              </div>
            </a-form-model-item>
          </a-form-model>
        </template>
      </a-modal>
    </div>
  </div>
</template>
<script type="text/ecmascript-6">
import axios from "axios";
import docCard from '../components/docCard.vue'
const data = [];
function myrefresh() {
  window.location.reload();
}
const plainOptions = ['edit', 'comment', 'share'];
const defaultCheckedList = ['edit', 'comment'];
export default {
  components: {
    docCard,
  },
  data() {
    return {
      templateValue:1,
      checkedList: defaultCheckedList,
      indeterminate: true,
      indeterminateTem: true,
      checkAll: false,
      plainOptions,
      newdocvisible:false,
      data,
      top: 0,
      visible: false,
      DocumentID: {
        type: Number,
      },
      newdocform:{
        title:"",
        modify_right:0,
        share_right:0,
        discuss_right:0,
        content:""
      },
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      content2:"# 欢迎使用 卷心菜文档模版1\n"+
        " ------\n"+
        "为了更好的使用文档,**graphene Markdown** 提供了两套模版系统 \n"+
        "> * 整理知识，学习笔记\n"+
        "> * 发布日记，杂文，所见所想\n"+
        "> * 撰写发布技术文稿（代码支持）\n"+
        "> * 撰写发布学术论文\n"+
        "![cmd-markdown-logo](https://www.zybuluo.com/static/img/logo.png)\n",
      content3:
        "# 欢迎使用 卷心菜文档模版2\n"+
        " ------\n"+
        "为了更好的使用文档,**graphene Markdown** 提供了两套模版系统 \n"+
        "以下是markdown简要使用说明\n"+
        "# Title1\n"+
        "## Title2\n"+
        "### Title3\n"+
        "content\n"+
        "==\n"+
        "content2\n"+
        "--\n"+
        "content3\n"+
        "--\n"+
        "* name\n"+
        "- name\n"+
        "+ name\n"+
        "* [I'm an inline-style link](https://www.google.com)\n"+
        "* Inline `code` has `back-ticks around` it.\n"+
        "```javascript\n"+
        "var s = \"JavaScript syntax highlighting\";\n"+
        "alert(s);\n"+
        "```"  
    };
  },
  methods: {
    successmsg(message) {
      this.$message.success(message);
    },
    errormsg(message) {
      this.$message.error(message);
    },
    onChange(checkedList) {
      this.indeterminate = !! checkedList.length && checkedList.length < plainOptions.length;
      this.checkAll = checkedList.length === plainOptions.length;
    },
    onChangeTem(e){
      console.log('radio checked',e.target.templateValue);
    },
    onCheckAllChange(e) {
      Object.assign(this, {
        checkedList: e.target.checked ? plainOptions : [],
        indeterminate: false,
        checkAll: e.target.checked,
      });
    },
    
    createdoc(){
      this.checkedList.forEach(element => {
        if(element=="edit")this.newdocform.modify_right=1;
        if(element=="comment")this.newdocform.discuss_right=1;
        if(element=="share")this.newdocform.share_right=1;
      });
      if (this.newdocform.title == ""){
              this.errormsg("empty title!");
              return;
            }
      switch(this.templateValue){
        case 1:
          break;
        case 2:
          this.newdocform.content=this.content2;
          break;
        case 3:
          this.newdocform.content=this.content3;
          break;
      }
      this.newdoc();
    },
    cancelcreate(){
      this.newdocvisible=false;
    },
    shownewdocform(){
      this.newdocvisible=true;
    },
    newdoc() {
      var _this=this;
      let formData = new FormData();
      formData.append("username", localStorage.getItem("token"));
      formData.append("title", this.newdocform.title);
      formData.append("modify_right", this.newdocform.modify_right);
      formData.append("share_right", this.newdocform.share_right);
      formData.append("discuss_right", this.newdocform.discuss_right);
      formData.append("content", this.newdocform.content);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios.post("http://localhost:5000/api/create_personal_doc/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
            _this.successmsg("successful create");
            setTimeout(() => {
              myrefresh();
            }, 2000);
          } 
          else {
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
    formData.append("username", localStorage.getItem("token"));
    let config = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };
    axios
      .post("http://localhost:5000/api/my_docs/", formData, config)
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