<template>
  <div class="movie-list-form">
    <button class="btn random-btn" 
    @click="getMovieList">다른 영화 불러오기</button>
    <div class="movie-list">
      <MovieCard 
      v-for="movie in movieRandomList"
      :key="movie.id"
      :movie="movie"
      @movie_detail="getDetailId" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import MovieCard from '@/components/MovieCard.vue'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieRandomList',
  components: {
    MovieCard,
  },
  data: function () {
    return {
      movieRandomList: [],
    }
  },
  created: function () {
    this.getMovieList()
  },
  methods: {
    getMovieList: function () {
      const MOVIE_URL = `${SERVER_URL}/movies/random/`
      axios.get(MOVIE_URL)
        .then(res => {
          console.log(res)
          this.movieRandomList = res.data
        })
        .catch(error => {
          console.log(error)
          this.movieRandomList = []
        })
    },
    getDetailId: function (data) {
      // console.log(data)
      this.$emit('movie_datail', data)
    }
  }
}
</script>

<style>
.movie-list {
  margin: 0 auto;
  margin-top: 1rem;
  padding: 0.5rem 2rem;
  display: flex;
  flex-wrap: wrap;
  text-align: center;
}

.movie-list-form {
  padding-left: 2rem;

}

.random-btn {
  width: 20rem;
  font-weight: 700;
  margin-top: 1rem;
  margin-right: 2rem;
  background-color: orangered;
}

.random-btn:hover {
  background-color: rgb(255, 145, 0);
}
</style>