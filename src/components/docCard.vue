<template>
  <a-card hoverable id="doc">
    <img
      slot="cover"
      alt="example"
      src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
    />
    <template slot="actions"> 
      <a-icon key="delete" type="delete" /> 
      <a-icon key="edit" type="edit" />
      <a-icon key="share" type="share-alt" />
    </template> 
    <a-card-meta :title="title" :description="editTime">
      <!-- <a-avatar
        slot="avatar"
        src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
      /> -->
    </a-card-meta>
  </a-card>
</template>


<script>
export default {
    name: "DocCard",
    data(){
        return{
            title: "文档标题",
            editTime: "编辑时间"
        }
    }
}
</script>

<style scoped>
#doc{
  width: 200px;
  height: 260px;
}
</style>