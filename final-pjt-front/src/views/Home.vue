<template>
  <div class="changesize d-flex flex-column justify-content-center align-items-center">
    <!-- <img src="@/../public/backgroundimg.jpg" alt=""> -->
    <h1>영화정보 및 리뷰를 한번에</h1>
    <h2>지금 바로 시작하세요</h2>
    <button class="btn" @click="goLogin">시작하기</button>
  </div>
  
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name : 'Home',
  data: function () {
    return {
      moviePlayingList: [],
    }
  },
  created: function () {
    this.getMovieList()
  },
  methods: {
    getMovieList: function () {
      const MOVIE_URL = `${SERVER_URL}/movies/playing/`
      axios.get(MOVIE_URL)
        .then(res => {
          // console.log(res)
          this.moviePlayingList = res.data
        })
        .catch(error => {
          console.log(error)
          this.moviePlayingList = []
        })
    },
    goLogin: function () {
      this.$router.push({name: 'Login'})
    }
  }
}
</script>

<style scoped>
  .changesize {
    height: 80vh;
    background-image: 
      url("../../public/backgroundimg.jpg");
    background-position: center;
  }

  .posterimg {
    opacity: 0.55;
  }

  .btn {
    display: inline-block;
    background-color: #F82F62;
    color: white;
    border-radius: 2vw;
  }

</style>