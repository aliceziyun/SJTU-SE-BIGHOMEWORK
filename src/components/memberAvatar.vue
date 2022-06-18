<template>
  <a-popover
    style="width: 40px"
    title="user info"
    trigger="hover"
    :visible="hovered"
    @visibleChange="handleHoverChange"
  >
    
      <div slot="content">
        <div>
            username:{{username}}
            <a slot="content" @click="gotoUserInfo"><br/>click this to get detailed information</a>
            <a slot="content" @click="sayhi" v-if="sayh"><br/>say "hi!"</a>
        </div>
      </div>
      <a-avatar :size="40"  style="margin-left:5px;margin-right:5px" @click="gotoUserInfo">{{username}}</a-avatar>
  </a-popover>
</template>
<script>
import axios from "axios";
export default {
  name: 'memberAvatar',

  props: {
    username: {
      type: String,
      default: 'not login',
      required: true,
    },
    icon: {
      type: String,
      default: 'user'
    }
  },

  data() {
    return {
      clicked: false,
      hovered: false,
      sayh:false,
    };
  },
  mounted(){
    if(this.username!=localStorage.getItem('token')){
      this.sayh=true;
    }
  },
  methods: {
    successmsg(message) {
      this.$message.success(message);
    },
    gotoUserInfo() {
      this.$router.push('/personal-page/'+this.username);
    },
    sayhi(){
      var _this=this
      let formData = new FormData();
      formData.append("sender_username",localStorage.getItem('token'));
      formData.append("receiver_username", this.username);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post("http://localhost:5000/api/sayhi/", formData, config)
        // eslint-disable-next-line
        .then(function (response) { 
            _this.successmsg("say 'hi' to your new friend!")
        })
        .catch(function (error) {
          console.log("Fail", error);
        });
    },
    handleHoverChange(visible) {
      this.clicked = false;
      this.hovered = visible;
    },
    handleClickChange(visible) {
      this.clicked = visible;
      this.hovered = false;
    },
  },
};
</script>