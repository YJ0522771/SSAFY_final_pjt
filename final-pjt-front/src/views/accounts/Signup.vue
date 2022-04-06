<template>
  <div class="bgimg d-flex justify-content-center align-items-center">
    <div class="loginform">
      <h3 class="mb-3">회원가입</h3>
      <div class="mb-3">
        <input type="email" class="form-control" placeholder="아이디"
          v-model="userData.username"
        >
        <p class="err" v-if="errMessageId">{{ errMessageId }}</p>
      </div>
      <div class="mb-3">
        <input type="password" class="form-control" placeholder="비밀번호"
          v-model="userData.password"
        >
      </div>
      <div class="mb-3">
        <input type="password" class="form-control" placeholder="비밀번호확인"
          @keypress.enter="signup"
          v-model="userData.passwordConfirmation"
        >
        <p class="err" v-if="errMessagePw">{{ errMessagePw }}</p>
      </div>
      <button class="btn" @click="signup">회원가입</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Signup',
  data: function () {
    return {
      userData: {
        username: null,
        password: null,
        passwordConfirmation: null,
      },
      errMessageId: '',
      errMessagePw: '',
    }
  },
  methods: {
    signup: function () {
      const SIGNUP_URL = `${SERVER_URL}/accounts/signup/`
      axios.post(SIGNUP_URL, this.userData)
        .then(res => {
          console.log(res)
          this.errMessageId = ''
          this.errMessagePw = ''
          this.$router.push({name: 'Login' })
        })
        .catch(err => {
          console.log(err.response)
          if (err.response.data.error) {
            this.errMessagePw = err.response.data.error
          } else {
            this.errMessagePw = null
          }
          if (err.response.data.username[0]) {
            this.errMessageId = err.response.data.username[0]
          } else {
            this.errMessageId = null
          }
        })
    }
  }
}
</script>

<style scoped>
  .err {
    color: red;
  }

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
</style>
