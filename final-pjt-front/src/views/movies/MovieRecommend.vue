<template>
  <div class="movie-list-form">
    <div class="recommend-list" v-if="isExists">
      <h3 class="genre-title" v-if="movieList123.length">#{{ genres[0] }}  #{{ genres[1] }}  #{{ genres[2] }}</h3>
      <div class="movie-list"
      v-if="movieList123.length">
        <MovieCard 
        v-for="movie in movieList123"
        :key="movie.id"
        :movie="movie"
        @movie_detail="getDetailId" />
      </div>

      <h3 class="genre-title" v-if="movieList12.length">#{{ genres[0] }}  #{{ genres[1] }}</h3>
      <div class="movie-list"
      v-if="movieList12.length">
        <MovieCard 
        v-for="movie in movieList12"
        :key="movie.id"
        :movie="movie"
        @movie_detail="getDetailId" />
      </div>

      <h3 class="genre-title" v-if="movieList13.length">#{{ genres[0] }}  #{{ genres[2] }}</h3>
      <div class="movie-list"
      v-if="movieList13.length">
        <MovieCard 
        v-for="movie in movieList13"
        :key="movie.id"
        :movie="movie"
        @movie_detail="getDetailId" />
      </div>

      <h3 class="genre-title" v-if="movieList23.length">#{{ genres[1] }}  #{{ genres[2] }}</h3>
      <div class="movie-list"
      v-if="movieList23.length">
        <MovieCard 
        v-for="movie in movieList23"
        :key="movie.id"
        :movie="movie"
        @movie_detail="getDetailId" />
      </div>
    </div>
    <p v-else>영화 추천을 위한 리뷰 정보가 부족합니다. (2개 이상 작성 권장)</p>
  </div>
</template>

<script>
import axios from 'axios'
import MovieCard from '@/components/MovieCard.vue'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieRecommend',
  components: {
    MovieCard,
  },
  data: function () {
    return {
      movieList123: [],
      movieList12: [],
      movieList13: [],
      movieList23: [],
      genres: [],
      isExists: true,
    }
  },
  created: function () {
    this.getMovieList()
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config= {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getMovieList: function () {
      const MOVIE_URL = `${SERVER_URL}/movies/recommend/`
      axios({
        method: 'get',
        url: MOVIE_URL,
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)
          this.isExists = res.data.exists
          console.log(res.data)

          if (this.isExists) {
            this.movieList123 = res.data.recommend123
            this.movieList12 = res.data.recommend12
            this.movieList13 = res.data.recommend13
            this.movieList23 = res.data.recommend23
            this.genres = res.data.best_genres
          }
        })
        .catch(error => {
          console.log(error)
          this.movieList123 = []
          this.movieList12 = []
          this.movieList13 = []
          this.movieList23 = []
        })
    },
    getDetailId: function (data) {
      console.log(data)
      this.$emit('movie_datail', data)
    }
  }
}
</script>

<style>
.recommend-list {
  text-align: start;
}

.genre-title {
  padding: 2rem 0 0 2rem;
  font-weight: bold;
}
</style>