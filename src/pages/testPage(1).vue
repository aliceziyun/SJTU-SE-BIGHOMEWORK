<template>
  <a-button @click="test()">测试</a-button>
</template>

<style>
#team-title {
  font-size: 40px;
  color: black;
}
</style>

<script>
export default {
  methods: {
    test() {
      var wsuri = "ws://127.0.0.1:8888/test";
      var websock = new WebSocket(wsuri);

      websock.onclose = function (e) {
        console.log(
          "websocket 断开: " + e.code + " " + e.reason + " " + e.wasClean
        );
        console.log(e);
      };
      console.log(websock);
    },
  },
};
</script>
