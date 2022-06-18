<template>
  <div>
    <a-list :grid="{ gutter: 25, xs: 1, sm: 2, md: 4, lg: 4, xl: 6, xxl: 6 }" :data-source="data">
      <a-list-item slot="renderItem" slot-scope="item">
        <docCard :docObj="item" :fav="4"></docCard>
      </a-list-item>
    </a-list>
  </div>
</template>

<script type="text/ecmascript-6">
import axios from "axios";
import docCard from '../components/docCard.vue';
const data = [];
export default {
  components: {
    docCard,
  },
  data() {
    return {
      data,
    };
  },
  methods: {
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
      .post("http://localhost:5000/api/my_deleted_docs/", formData, config)
      .then(function (response) {
        if (response) {
          _this.data = response.data;
          console.log(response.data);
        } else {
          alert("please log first!");
        }
      })
      .catch(function (error) {
        console.log("wrong", error);
      });
  },
};
</script>