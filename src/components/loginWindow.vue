<template>
  <section>
    <div class="container">
      <div class="user signinBx">
        <div class="imgBx"><img src="@/assets/cabbage2.jpg" /></div>
        <div class="formBx">
          <a-form-model ref="loginForm" :model="loginForm">
            <h2>Sign In</h2>
            <a-input
              type="text"
              placeholder="Username"
              v-model="loginForm.username"
            />
            <a-input
              type="password"
              placeholder="Password"
              v-model="loginForm.password"
            />
            <input type="submit" value="Login" @click="checklogin()" />
            <p class="signup">
              Don't have an account?
              <a href="#" @click="removeForm()">Sign up.</a>
            </p>
          </a-form-model>
        </div>
      </div>
      <div class="user signupBx">
        <div class="formBx">
          <a-form-model ref="ruleForm" :model="ruleForm" :rules="rules">
            <h2>Create an account</h2>
            <a-form-model-item has-feedback prop="username">
              <a-input
                type="text"
                placeholder="Username"
                v-model="ruleForm.username"
              />
            </a-form-model-item>
            <a-form-model-item has-feedback prop="email">
              <a-input
                type="text"
                placeholder="Email Address"
                v-model="ruleForm.email"
              />
            </a-form-model-item>
            <a-form-model-item has-feedback prop="pass">
              <a-input
                type="password"
                placeholder="Create Password"
                v-model="ruleForm.pass"
              />
            </a-form-model-item>
            <a-form-model-item has-feedback prop="checkPass">
              <a-input
                type="password"
                placeholder="Confirm Password"
                v-model="ruleForm.checkPass"
              />
            </a-form-model-item>
            <input type="submit" value="Sign Up" @click="signup('ruleForm')"/>
            <p class="signup" >
              Already have an account?
              <a href="#" @click="toggleForm()">Sign in.</a>
            </p>
          </a-form-model>
        </div>
        <div class="imgBx"><img src="@/assets/cabbage1.jpg" /></div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
function myrefresh() {
  window.location.reload();
}
export default {
  name: "loginWindow",
  data() {
    let validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("please input your password!"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    let validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("please input your password!"));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error("two input password must be same!"));
      } else {
        callback();
      }
    };
    let validateusername = (rule, value, callback) => {
      if (value == "") {
        callback(new Error("empty username!"));
      } else {
        callback();
      }
    };
    let validateemail = (rule, value, callback) => {
      if (value == "") {
        callback(new Error("empty email address!"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        pass: "",
        checkPass: "",
        email: "",
        username: "",
      },
      loginForm: {
        username: "",
        password: "",
      },
      rules: {
        pass: [{ validator: validatePass, trigger: "change" }],
        checkPass: [{ validator: validatePass2, trigger: "change" }],
        username: [{ validator: validateusername, trigger: "change" }],
        email: [{ validator: validateemail, trigger: "change" }],
      },
      wronglog: {
        wl: false,
      },

      rightlog: {
        rl: false,
      },
    };
  },
  methods: {
    successmsg(message) {
      this.$message.success(message);
    },
    errormsg(message) {
      this.$message.error(message);
    },
    removeForm() {
      let section = document.querySelector("section");
      let container = document.querySelector(".container");
      container.classList.toggle("active");
      section.classList.toggle("active");
    },
    toggleForm() {
      let section = document.querySelector("section");
      let container = document.querySelector(".container");
      container.classList.toggle("active");
      section.classList.toggle("active");
    },
    callback(key) {
      console.log(key);
    },
    successmessage(msg) {
      this.$message.success(msg);
    },
    errormessage(msg) {
      this.$message.error(msg);
    },
    signup(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let formData = new FormData();
          formData.append("username", this.ruleForm.username);
          formData.append("password", this.ruleForm.pass);
          formData.append("email", this.ruleForm.email);
          let config = {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          };
          var _this = this;
          axios
            .post("http://localhost:5000/api/regist/", formData, config)
            .then(function (response) {
              if (response.data.message == "success") {
                _this.successmessage("注册成功");
                setTimeout(() => {
                  myrefresh();
                }, 2000);
              } else if (response.data.message == "fail") {
                _this.errormessage("existed username & email!");
              } else {
                _this.errormessage("未知错误，请稍后再试");
              }
            })
            .catch(function () {
              _this.errormessage("未知错误，请稍后再试");
            });
        } else {
          return false;
        }
      });
    },
    checklogin() {
      console.log("用户登录");
      let formData = new FormData();
      formData.append("username", this.loginForm.username);
      formData.append("password", this.loginForm.password);
      let config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      var _this = this;
      axios
        .post("http://localhost:5000/api/login/", formData, config)
        .then(function (response) {
          if (response.data.message != "fail") {
            _this.successmessage("successful login!")
            localStorage.setItem("token", _this.loginForm.username);
            localStorage.setItem("userid", response.data.id);
            console.log("用户登录" + localStorage.getItem("userid"));
            _this.$router.push("/home");
          } else {
            _this.errormessage("invalid username or password!");
          }
        })
        .catch(function () {
          _this.errormessage("未知错误，请稍后再试");
        });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>

<style scoped>
section {
  overflow: hidden;
  position: relative;
  min-height: 100vh;
  background: #85b1a6;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  margin-top: 0%;
  transition: 0.5s;
}
section.active {
  background: #436860;
}
section .container {
  position: relative;
  width: 800px;
  height: 500px;
  background: #fff;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
section .container .user {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
}
section .container .user .imgBx {
  position: relative;
  width: 50%;
  height: 100%;
  transition: 0.5s;
}
section .container .user .imgBx img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
section .container .user .formBx {
  position: relative;
  width: 50%;
  height: 100%;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  transition: 0.5s;
}

section .container .user .formBx form {
  text-align: center;
}

section .container .signinBx h2 {
  font-size: 2.5rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  width: 100%;
  margin-top: 10px;
  margin-bottom: 10px;
  color: #555;
}

section .container .signupBx h2 {
  font-size: 1.6rem;
  font-weight: 660;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  width: 100%;
  margin-top: 10px;
  margin-bottom: 10px;
  color: #555;
}

section .container .user .formBx input {
  width: 100%;
  padding: 10px;
  background: #f5f5f5;
  color: #333;
  border: none;
  outline: none;
  font-size: 14px;
  margin: 8px 0;
  letter-spacing: 1px;
  font-weight: 300;
}
section .container .user .formBx input[type="submit"] {
  max-width: 100px;
  background: #27ae60;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 1px;
  transition: 0.5s;
}
section .container .user.signupBx .formBx input[type="submit"] {
  background: #27ae60;
}
section .container .user .formBx .signup {
  position: relative;
  margin-top: 10px;
  font-size: 12px;
  letter-spacing: 1px;
  color: #555;
  text-transform: uppercase;
  font-weight: 300;
}
section .container .user .formBx .signup a {
  font-weight: 600;
  text-decoration: none;
  color: #27ae60;
}
section .container .signupBx {
  pointer-events: none;
}
section .container.active .signupBx {
  pointer-events: initial;
}
section .container .signupBx .formBx {
  top: 100%;
}
section .container.active .signupBx .formBx {
  top: 0;
}
section .container .signupBx .imgBx {
  top: -100%;
  transition: 0.5s;
}
section .container.active .signupBx .imgBx {
  top: 0;
}
section .container .signinBx {
  top: 0;
}
section .container.active .signinBx .formBx {
  top: 100%;
}
section .container .imgBx {
  top: 0;
  transition: 0.5s;
}
section .container.active .signinBx .imgBx {
  top: -100%;
}
@media (max-width: 991px) {
  section .container {
    max-width: 400px;
  }
  section .container .imgBx {
    display: none;
  }
  section .container .user .formBx {
    width: 100%;
  }
  section .container.active .signinBx .formBx {
    top: -100%;
  }
}
</style>
