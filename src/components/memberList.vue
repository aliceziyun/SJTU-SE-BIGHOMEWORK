<template>
<div>
  <a-col align='center'>
  <p v-if="hasMember">无可分享对象</p>
  <span v-for="(user,index) in memberList" :key="index">
    <memberAvatar :username="user.username"></memberAvatar>
  </span>
  </a-col>
</div>
</template>

<script>

import memberAvatar from './memberAvatar';
import axios from 'axios';

export default{
  name: 'memberList',

  props: {
    propGroupid: {
      type: Number,
    },
  },

  watch: {
    propGroupid: {
      handler(newVal) {
        this.groupid=newVal;
      },
      deep: true,
      immediate: true,
    }
  },

  data(){
    return{
      groupid:'',
      memberList: [],
      hasMember: true,
    };
    
  },

  components: {
    memberAvatar,
  },

  mounted(){
    this.memberList=[];
    let formData=new FormData();
    formData.append('groupid',this.groupid);
    let config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    };
    var _this=this;
    axios.post('http://localhost:5000/api/get_user_bygroup/',formData,config)
      .then(function(response) {
        if(response) {
          _this.memberList=response.data;
        }
      }).catch(error=> {
        console.log('error',error);
      })
    if(this.memberList.length != 0)
        this.hasMember = false;
  }
}

</script>
<style></style>