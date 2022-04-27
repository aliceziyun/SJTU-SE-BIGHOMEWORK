<template>
  <div id="userpage">
    <section class="newsletter">
      <div class="backarrow">
        <a @click="Back()"><i class="fa fa-arrow-left"></i></a>
      </div>
      <div class="header">
        <img src="@/assets/icon.png" alt="" />
        <h3>{{ userObj.username }}</h3>
        <p>This is a brief introduction.</p>
      </div>
      <div class="numbers">
        <div class="num">
          <h3>{{ mydocs }}</h3>
          <p>Files</p>
        </div>
        <div class="num">
          <h3>{{ mydocs }}</h3>
          <p>Host</p>
        </div>
        <div class="num">
          <h3>0</h3>
          <p>Participate</p>
        </div>
      </div>
    </section>
    <section class="details" id="details">
      <h3>Account Settings</h3>
      <p>
        Add another email address to your account to access any upgrades to your
        university or institution, make it easier for partners to find you and
        ensure that you can restore your account.
      </p>
      <p>
        To change your primary email, please add your new primary email address
        first (by clicking Add another email) and confirm it. Then click the
        Modify button.
      </p>
      <hr />
    </section>
    <section class="footer">
      <div class="box-container">
        <div class="box">
          <h3>Get rapid contact</h3>
          <p>You can quickly contact the author via the following ways.</p>
          <a href="#">
            <i class="fa fa-phone" style="color: #27ae60"></i> +123-456-7890
          </a>
          <a href="#">
            <i class="fa fa-envelope" style="color: #27ae60"></i
            >{{ userObj.email }}</a
          >
        </div>

        <div class="box">
          <h3>Detailed information</h3>
          <p>
            To get faster and more efficient cooperation, you can get some
            information below.
          </p>
          <a href="#">
            <i class="fa fa-arrow-right" style="color: #27ae60"></i> Nick Name
          </a>
          <a href="#">
            <i class="fa fa-arrow-right" style="color: #27ae60"></i> Gender
          </a>
          <a href="#">
            <i class="fa fa-arrow-right" style="color: #27ae60"></i> Profession
          </a>
          <a href="#">
            <i class="fa fa-arrow-right" style="color: #27ae60"></i> Institution
          </a>
          <a href="#">
            <i class="fa fa-arrow-right" style="color: #27ae60"></i> Blogs
          </a>
        </div>
      </div>
      <div class="modify">
        <button type="primary" id="change-button">
          <p>Modify your information</p>
        </button>
        <button type="primary" id="exit" @click="Logout()">
          <p>Log out</p>
        </button>
      </div>

      <div class="share">
        <a href="#"
          ><QqCircleFilled style="fontsize: 2rem; color: #27ae60"
        /></a>
        <a href="#"
          ><WeiboCircleFilled style="fontsize: 2rem; color: #27ae60"
        /></a>
        <a href="#"><GithubFilled style="fontsize: 2rem; color: #27ae60" /></a>
        <a href="#"><WechatFilled style="fontsize: 2rem; color: #27ae60" /></a>
        <a href="#"
          ><FacebookFilled style="fontsize: 2rem; color: #27ae60"
        /></a>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import {
  QqCircleFilled,
  WeiboCircleFilled,
  GithubFilled,
  WechatFilled,
  FacebookFilled,
} from "@ant-design/icons-vue";
export default {
  name: "userHome",
  components: {
    QqCircleFilled,
    WeiboCircleFilled,
    GithubFilled,
    WechatFilled,
    FacebookFilled,
  },

  data() {
    return {
      loading: false,
      disabled: false,

      userObj: {
        username: "",
        email: "",
        description: "",
      },
      mydocs: 0,
    };
  },
  methods: {
    Logout() {
      this.$router.push("/");
    },
    Back(){
      this.$router.push("/home");
    }
  },

  mounted() {
    let formData = new FormData();
    formData.append("username", this.$route.params.username);
    console.log(this.$route.params.username);
    let config = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };
    var _this = this;
    axios
      .post("http://localhost:5000/api/get_user/", formData, config)
      .then(function (response) {
        if (response) {
          _this.userObj = response.data;
        }
      })
      .catch((error) => {
        console.log("error", error);
      });
    axios
      .post("http://localhost:5000/api/my_docs/", formData, config)
      .then(function (response) {
        if (response) {
          _this.mydocs = response.data.length;
          console.log(response.data.length);
        }
      })
      .catch((error) => {
        console.log("error", error);
      });
  },
};
</script>

<style scoped>
#userpage {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  text-align: center;
  margin: 0;
  padding: 0;
  outline: none;
  border: none;
}

:root {
  --green: #27ae60;
  --dark-color: #219150;
  --black: #444;
  --light-color: #666;
  --border: 0.1rem solid rgba(0, 0, 0, 0.1);
  --border-hover: 0.1rem solid var(--black);
  --box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.newsletter {
  background: url(@/assets/cabbage4.png) no-repeat;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  background-color: rgba(0, 0, 0, 0.25);
}

.newsletter .backarrow{
    height: 2.8rem;
    width: 2.8rem;
    text-align: left;
    margin-left: 1.4rem;
}

.newsletter .backarrow a i{
    color:#fff;
    font-size: 1.4rem;
    margin-top: 1.4rem;
}

.newsletter .backarrow a i:hover{
    color: #27ae60;
}

.newsletter .header {
  max-width: 45rem;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  padding: 5rem 0;
}

.newsletter .header img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.newsletter .header h3 {
  font-size: 3.2rem;
  color: #fff;
  font-weight: bold;
  margin-top: 2.8rem;
  margin-bottom: 0.4rem;
}

.newsletter .header p {
  margin-top: 0;
  padding-top: 0;
  color: #fff;
  font-size: 1.5rem;
}

.newsletter .numbers {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
  gap: 1.5rem;
  color: #fff;
}

.newsletter .numbers .num h3 {
  font-size: 1.8rem;
  margin-bottom: 0.8rem;
  color: #fff;
}

.newsletter .numbers .num p {
  font-size: 1.2rem;
  margin-top: 0;
}

.details {
  text-align: center;
}

.details h3 {
  font-size: 2rem;
  color: var(--black);
  padding-top: 0;
  line-height: 2.2rem;
  font-weight: bold;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.details p {
  color: #666;
  font-size: 1rem;
}

.details hr {
  position: relative;
  width: 95%;
  margin: 18px auto;
  border: none;
  border-top: 1px solid #666;
  text-align: center;
}

.footer .box-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(25rem, 1fr));
  gap: 1.5rem;
}

.footer .box-container .box h3 {
  font-size: 2.2rem;
  color: var(--black);
  margin-bottom: 0;
  font-weight: bold;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.footer .box-container .box p {
  color: #666;
  font-size: 1.2rem;
  padding: 0 1.2rem;
}

.footer .box-container .box a {
  display: block;
  font-size: 1.4rem;
  color: var(--black);
  padding: 1rem 0;
  outline: none;
}

.footer .box-container .box a i {
  color: var(--green);
  padding-right: 0.5rem;
}

.footer .box-container .box a:hover i {
  padding-right: 2rem;
}

.footer .box-container .box .map {
  width: 100%;
}

.footer .share {
  padding: 1rem 0;
  text-align: center;
}

.footer .share a {
  height: 3rem;
  width: 3rem;
  line-height: 3rem;
  font-size: 2rem;
  color: #fff;
  background: var(--green);
  margin: 0.3rem;
  border-radius: 50%;
}

.footer .share a:hover {
  background: var(--black);
}

.footer .modify {
  display: grid;
  gap: 1.5rem;
  line-height: 1.2rem;
}

.footer .modify #change-button {
  font-size: 1.2rem;
  margin-top: 8px;
  color: #fff;
  background: #27ae60;
  padding-left: 0.7rem;
  padding-right: 0.7rem;
  height: 4rem;
  border: none;
  border-radius: 9999px;
}

.footer .modify #change-button p {
  margin-top: 1.2rem;
  margin-bottom: 2rem;
}

.footer .modify #change-button:hover {
  background: #219150;
  cursor: pointer;
}

.footer .modify #exit {
  font-size: 1.2rem;
  margin-top: 8px;
  color: #fff;
  background: #666;
  padding-left: 0.7rem;
  padding-right: 0.7rem;
  border: none;
  border-radius: 9999px;
  height: 4rem;
}

.footer .modify #exit p {
  margin-top: 1.2rem;
  margin-bottom: 2rem;
}

.footer .modify #exit:hover {
  background: #444;
  cursor: pointer;
}

.footer .credit {
  border-top: var(--border);
  padding: 0 1rem;
  padding-top: 0.5rem;
  font-size: 1rem;
  color: var(--light-color);
  text-align: center;
}

.footer .credit span {
  color: var(--green);
}
</style>
