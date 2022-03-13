<template>
<a-layout>
    <a-layout-header style="background:white">
        <a-input-search placeholder="查询团队" style="width:300px;margin-left:600px;margin-top:25px;" @search="onSearch" />
    </a-layout-header>

    <a-layout-content style="background:white">
        <a-card style="width:1200px;height:500px;margin:50px auto;">
            <a-collapse v-model="activeKey" :expand-icon-position="expandIconPosition">
                <a-collapse-panel key="1" header="团队1">
                    <p>{{text}}</p>
                    <a-icon slot="extra" type="delete" @click="handleClick" style="margin-right:10px;fontSize:20px" />
                    <a-icon slot="extra" type="plus" @click="handleClick" style="margin-right:10px;fontSize:20px" />
                    <a-icon slot="extra" type="setting" @click="handleClick" style="margin-right:0px;fontSize:20px"/>
                </a-collapse-panel>
                <a-collapse-panel key="2" header="团队2">
                    <p>{{text}}</p>
                </a-collapse-panel>
                <a-collapse-panel key="3" header="团队3">
                    <p>{{text}}</p>
                </a-collapse-panel>
            </a-collapse>
        </a-card>
    </a-layout-content>
</a-layout>
</template>

<style>
#team-title{
    font-size: 40px;
    color: black;
}
</style>

<script>
export default {
  data() {
    return {
      text:'还没整，不急哈',
    };
  },
};
</script>
