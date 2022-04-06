<template>
<div class="bgimg d-flex justify-content-center align-items-center">
  <div class="loginform">
    <h3 class="mb-3">로그인</h3>
    <div class="mb-3">
    <input type="email" class="form-control" placeholder="아이디"
      v-model="userData.username"
    >
  </div>
  <div class="mb-3">
    <input type="password" class="form-control" placeholder="비밀번호"
      @keypress.enter="login"
      v-model="userData.password"
    >
  </div>
  <p class="err text-danger">{{errmessage}}</p>
  <button class="btn" @click="login">로그인</button>
  <p class="signup mt-3">
    Kinesis회원이 아닌가요? 
    <router-link :to="{ name: 'Signup' }">지금가입하세요</router-link>
  </p>
    <!-- <h1>Login</h1>
    <div>
      <label for="username">사용자 이름: </label>
      <input type="text" id="username" v-model="userData.username">
    </div>
    <div>
      <label for="password">비밀번호: </label>
      <input type="password" id="password" v-model="userData.password"
        @keypress.enter="login"
      >
    </div>
    <button @click="login">Login</button>
    <p class="text-danger">{{errmessage}}</p>
    <p>아직회원이 아니신가요? 
      <router-link :to="{ name: 'Signup' }">회원가입</router-link>
    </p> -->
  </div>
</div>
  
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Login',
  data: function () {
    return {
      userData: {
        username: null,
        password: null,
      },
      errmessage: null,
    }
  },
  methods: {
    login: function () {
      axios.post(`${SERVER_URL}/accounts/login/`, this.userData)
        .then(res => {
          // console.log(res.data.token)
          this.errmessage = null
          localStorage.setItem('jwt', res.data.token)
          this.$emit('login')
          this.$router.push({ name: 'MovieList' })
        })
        .catch(err => {
          // console.log(err.response.data.non_field_errors[0])
          if (err.response.data.non_field_errors[0]) {
            this.errmessage = '아이디 혹은 비밀번호를 잘못입력하셨습니다.'
          }
        })
    }
  }
}
</script>

<style scoped>
  .loginform {
    width: 400px;
    height: 40vh;
    padding: 60px 68px 40px;
    background-color: rgb(32, 37, 44);
    border-radius: 4px;
  }

  .bgimg {
    height: 80vh;
    background:
      center/80% 
      url("../../../public/loginbackgroundimg.jpg");
  }

  .btn {
    width: 100%;
    background-color: #F82F62;
    color: white;
  }

  .signup {
    font-size: 14px;
  }

  .err {
    font-size: 12px;
  }
</style>
