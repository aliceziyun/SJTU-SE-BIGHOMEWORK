<template>
  <div class="notice-box">
    <a-modal
      title="Send message to user"
      :visible="messagebox"
      @ok="SendMessage()"
      @cancel="cancelMessage"
    >
      <template>
        <a-input
          v-model="my_message"
          placeholder="Please type your message"
        />
      </template>
    </a-modal>
    <a-table
      :columns="columns"
      :data-source="data"
      style="margin-right:170px;margin-top:30px"
      rowKey="id"
    >v
      <a slot="name" slot-scope="text">{{ text }}</a>
      <span slot="customTitle"></span>
      <span slot="action" slot-scope="text,item">
        <a-button type="primary" size="small" @click="agree_invitation(item.id)">
          check
        </a-button>
        <a-button size="small" @click="Message(item.sender_name)">
          reply
        </a-button>
        <a>{{ item.blank }}</a>
      </span>
    </a-table>
  </div>
</template>

<style scoped>
.notice-box{
  width:1150px;
  margin-left: 100px;
}
</style>

<script type="text/ecmascript-6">
import axios from "axios";
const columns = [
  {
    title: "CONTENT",
    dataIndex: "content",
    key: "content",
    width: 450,
  },
  {
    title: "DATATIME",
    dataIndex: "datetime",
    key: "datetime",
    width: 350,
  },
  {
    title: "ACTION",
    key: "action",
    scopedSlots: { customRender: "action" },
    width: 150,
  },
];

const data = [];
export default {
  data() {
    return {
      data,
      columns,
      messagebox:false,
      sender:"",
    };
  },
  mounted: function () {
    this.get_confirm_notice();
  },
  methods: {
    get_confirm_notice() {
      let formData = new FormData();
      formData.append("receiver_username", localStorage.getItem("token"));
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      var _this = this;
      axios
        .post(
          "http://192.168.1.111:5000/api/view_message/",
          formData,
          config
        )
        .then(function (response) {
          console.log(response.data);
          _this.data = response.data;
        })
        .catch(function (error) {
          console.log("Fail", error);
        });
    },

    agree_invitation(id) {
      var _this = this;
      var item = this.data.find((item) => item.id == id);
      let formData = new FormData();
      formData.append("new_notice_id", item.id);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://192.168.1.111:5000/api/del_new_notice/", formData, config)
        .then(function (response) {
          console.log(response.data.message);
          _this.data=_this.data.filter((record)=>record.id!=item.id);
          _this.$emit('updatenotice');
        })
        .catch(function (error) {
          console.log("Fail", error);
        });
    },
    successmsg(message) {
      this.$message.success(message);
    },
    errormsg(message) {
      this.$message.error(message);
    },
    Message(name) {
      this.messagebox = true;
      this.sender = name;
    },
    cancelMessage() {
      this.messagebox = false;
    },
    SendMessage(){
      var _this = this;
      let formData = new FormData();
      console.log(this.sender);
      formData.append("receiver", this.sender);
      formData.append("sender", localStorage.getItem("token"));
      formData.append("message", this.my_message);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://192.168.1.111:5000/api/message_user/", formData, config)
        .then(function (response) {
          if (response.data.message == "success") {
            _this.successmsg("successful message");
            setTimeout(() => {
                _this.messagebox=false;
              }, 1000);
          } 
          else {
            _this.errormsg("message fail!");
          }
        })
        .catch(function () {
          _this.errormsg("message fail,please try later!");
        });
    },
  },
};
</script>