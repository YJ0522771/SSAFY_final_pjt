<template>
  <div id="app">
    <div class="main-nav d-flex align-items-center justify-content-be">
      <img src="../public/logo.png" 
        alt="logo"
        class="logo"
        @click="goPage">
      <div v-if="isLogin" class="flex-grow-1 d-flex collapse navbar-collapse justify-content-between">
        <div>
          <router-link :to="{ name: 'MovieList' }" 
          class="nav-item">
          <i class="fas fa-film"></i>
          Movie List</router-link>
          <router-link :to="{ name: 'MovieRecommend' }"
          class="nav-item">
          <i class="far fa-thumbs-up"></i>
          Recommend</router-link>
        </div>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="fas fa-user"></i> {{ username }}
          </a>
          <ul class="dropdown-menu nav-dropdown" aria-labelledby="navbarDropdown">
            <li class="nav-dropdown-menu">
              <router-link :to="{ name: 'Profile', params: { username: username }}" style="font-size: 16px;">내 프로필</router-link>
            </li>
            <li class="nav-dropdown-menu">
              <router-link @click.native="logout" to="#" style="font-size: 16px;">로그아웃</router-link>
            </li>
          </ul>
        </li> 
          
          <!-- <router-link :to="{ name: 'Profile', params: { username: username }}">{{ username }}</router-link>  -->
          <!-- <router-link @click.native="logout" to="#" class="logoutstate ms-auto">로그아웃</router-link> -->
          <!-- <p>안녕하세요 {{username}}님</p> -->
      </div>
      <div v-else class="flex-grow-1 d-flex justify-content-between">
        <p></p>
        <!-- <router-link :to="{ name: 'Signup' }">Signup</router-link>  -->
        <router-link :to="{ name: 'Login' }" id="" class="nav-item">
        <i class="fas fa-user"></i>
        Login</router-link> 
      </div>
      
        
    </div>
    <router-view 
    @login="login"
    @movie_datail="goDetail" />
  </div>
</template>

<script>
import jwt_decode from "jwt-decode";

// const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'App',
  data: function () {
    return {
      isLogin: false,
      username: '',
    }
  },
  methods: {
    logout: function () {
      this.isLogin = false
      localStorage.removeItem('jwt')
      this.$router.push({ name: 'Login' })
    },
    login: function () {
      this.isLogin = true
      const token = localStorage.getItem('jwt')
      let decoded = jwt_decode(token)
      this.username = decoded.username
    },
    // 영화 상세 정보 페이지로
    goDetail: function (data) {
      this.$router.push({
        name: 'MovieDetail',
        params: {
          id: data
        }
      })
    },
    goPage: function () {
      const token = localStorage.getItem('jwt')
      if (token) {
        this.$router.push({name: 'MoviePlayingList'})
      } else {
        this.$router.push({name: 'Home'})
      }
    }
  },
  created: function () {
    const token = localStorage.getItem('jwt')
    if (token) {
      this.isLogin = true
      let decoded = jwt_decode(token)
      console.log(decoded)
      this.username = decoded.username
      this.$router.push({name: 'MoviePlayingList'})
    } else {
      this.$router.push({name: 'Home'})
    }

    // window.addEventListener('beforeunload', this.logout)
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  
}

.main-nav {
  margin-bottom: 1rem;
  padding: 0 10px 0 10px;
  width: 100%;
  list-style:none;
}

.main-nav a {
  font-weight: bold;
  font-size: 22px;
  color: rgb(243, 255, 250);
  text-decoration: none;
  margin: 0 1rem;
}

.main-nav a.router-link-exact-active {
  color: red;
}

.nav-dropdown {
  background-color: cadetblue;
}

.nav-dropdown-menu {
  padding: 2px 0;
}

.nav-dropdown-menu:hover {
  background-color: rgb(130, 220, 223);
  text-decoration-line: underline;
}

.logo {
  width: 200px;
  height: 100px;
  margin-right: 10px;
  cursor: pointer;
}

.logoutstate {
  background-color: red;
  line-height: normal;
  padding: 7px 17px;
  font-weight: 400;
  font-size: 1rem;
  margin-right: 80px;
}

#loginstate {
  background-color: green ;
  color: white;
  line-height: normal;
  padding: 7px 17px;
  font-weight: 400;
  font-size: 1rem;
  margin-right: 80px;
}



body {
  background-color: rgb(32, 37, 44);
  color: rgb(199, 224, 214);
}

ul {
  list-style:none;
  padding-left:0px;
}


</style>
