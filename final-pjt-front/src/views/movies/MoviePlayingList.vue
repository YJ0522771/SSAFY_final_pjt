<template>
  <div class="movie-list-form">
    <div class="movie-list">
      <MovieCard 
      v-for="movie in moviePlayingList"
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
  name: 'MoviePlayingList',
  components: {
    MovieCard,
  },
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
          console.log(res)
          this.moviePlayingList = res.data
        })
        .catch(error => {
          console.log(error)
          this.moviePlayingList = []
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

</style>